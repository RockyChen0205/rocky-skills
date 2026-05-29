import { defineCommand } from '../../command';
import { CLIError } from '../../errors/base';
import { ExitCode } from '../../errors/codes';
import { requestJson } from '../../client/http';
import { videoGenerateEndpoint, videoTaskEndpoint, fileRetrieveEndpoint } from '../../client/endpoints';
import { poll } from '../../polling/poll';
import { downloadFile, formatBytes } from '../../files/download';
import { formatOutput, detectOutputFormat } from '../../output/formatter';
import type { Config } from '../../config/schema';
import type { GlobalFlags } from '../../types/flags';
import type { VideoRequest, VideoResponse, VideoTaskResponse, FileRetrieveResponse } from '../../types/api';
import { readFileSync } from 'fs';
import { extname } from 'path';

const MIME_TYPES: Record<string, string> = {
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.png': 'image/png', '.webp': 'image/webp',
};
import { isInteractive } from '../../utils/env';
import { promptText, failIfMissing } from '../../utils/prompt';

export default defineCommand({
  name: 'video generate',
  description: 'Generate a video (Hailuo-2.3 / 2.3-Fast)',
  usage: 'mmx video generate --prompt <text> [flags]',
  options: [
    { flag: '--model <model>', description: 'Model ID (default: MiniMax-Hailuo-2.3)' },
    { flag: '--prompt <text>', description: 'Video description', required: true },
    { flag: '--first-frame <path-or-url>', description: 'First frame image' },
    { flag: '--callback-url <url>', description: 'Webhook URL for completion notification' },
    { flag: '--download <path>', description: 'Save video to file on completion' },
    { flag: '--no-wait', description: 'Return task ID immediately without waiting' },
    { flag: '--async', description: 'Return task ID immediately (agent/CI mode, same as --no-wait but explicit)' },
    { flag: '--poll-interval <seconds>', description: 'Polling interval when waiting (default: 5)', type: 'number' },
  ],
  examples: [
    'mmx video generate --prompt "A man reads a book. Static shot."',
    'mmx video generate --prompt "Ocean waves at sunset." --download sunset.mp4',
    'mmx video generate --prompt "A robot painting." --async --quiet',
    'mmx video generate --prompt "A robot painting." --no-wait --quiet',
  ],
  async run(config: Config, flags: GlobalFlags) {
    let prompt = flags.prompt as string | undefined;

    if (!prompt) {
      if (isInteractive({ nonInteractive: config.nonInteractive })) {
        const hint = await promptText({ message: 'Enter your video prompt:' });
        if (!hint) {
          process.stderr.write('Video generation cancelled.\n');
          process.exit(1);
        }
        prompt = hint;
      } else {
        failIfMissing('prompt', 'mmx video generate --prompt <text>');
      }
    }

    const model = (flags.model as string) || 'MiniMax-Hailuo-2.3';
    const format = detectOutputFormat(config.output);

    const body: VideoRequest = {
      model,
      prompt,
    };

    if (flags.firstFrame) {
      const framePath = flags.firstFrame as string;
      if (framePath.startsWith('http')) {
        body.first_frame_image = framePath;
      } else {
        const imgData = readFileSync(framePath);
        const ext = extname(framePath).toLowerCase();
        const mime = MIME_TYPES[ext] || 'image/jpeg';
        body.first_frame_image = `data:${mime};base64,${imgData.toString('base64')}`;
      }
    }

    if (flags.callbackUrl) {
      body.callback_url = flags.callbackUrl as string;
    }

    if (config.dryRun) {
      console.log(formatOutput({ request: body }, format));
      return;
    }

    const url = videoGenerateEndpoint(config.baseUrl);
    const response = await requestJson<VideoResponse>(config, {
      url,
      method: 'POST',
      body,
    });

    const taskId = response.task_id;

    if (!config.quiet && !flags.noWait && !config.async) {
      process.stderr.write(`[Model: ${model}]\n`);
    } else if (!config.quiet) {
      process.stderr.write(`[Model: ${model}]\n`);
    }

    // --no-wait or --async: return task ID immediately
    if (flags.noWait || config.async) {
      // Always pure JSON — Agent/CI mode needs predictable stdout
      process.stdout.write(JSON.stringify({ taskId }));
      process.stdout.write('\n');
      return;
    }

    // Default: poll until completion
    const pollInterval = (flags.pollInterval as number) ?? 5;
    const taskUrl = videoTaskEndpoint(config.baseUrl, taskId);

    const result = await poll<VideoTaskResponse>(config, {
      url: taskUrl,
      intervalSec: pollInterval,
      timeoutSec: config.timeout,
      isComplete: (d) => (d as VideoTaskResponse).status === 'Success',
      isFailed: (d) => (d as VideoTaskResponse).status === 'Failed',
      getStatus: (d) => (d as VideoTaskResponse).status,
    });

    if (!result.file_id) {
      throw new CLIError(
        'Task completed but no file_id returned.',
        ExitCode.GENERAL,
      );
    }

    // Resolve file_id to download URL
    const fileInfo = await requestJson<FileRetrieveResponse>(config, {
      url: fileRetrieveEndpoint(config.baseUrl, result.file_id),
    });
    const downloadUrl = fileInfo.file?.download_url;

    if (!downloadUrl) {
      throw new CLIError(
        'No download URL available for this file.',
        ExitCode.GENERAL,
      );
    }

    // --download: save to file
    if (flags.download) {
      const destPath = flags.download as string;
      const { size } = await downloadFile(downloadUrl, destPath, { quiet: config.quiet });

      if (config.quiet) {
        console.log(destPath);
      } else {
        console.log(formatOutput({
          task_id: taskId,
          status: 'Success',
          file_id: result.file_id,
          saved: destPath,
          size: formatBytes(size),
        }, format));
      }
      return;
    }

    // Default: auto-download to temp location and output local file path
    const os = await import('os');
    const { join } = await import('path');
    const destDir = join(os.tmpdir(), 'mmx-video');
    const { existsSync, mkdirSync } = await import('fs');
    if (!existsSync(destDir)) mkdirSync(destDir, { recursive: true });
    const destPath = join(destDir, `${taskId}.mp4`);

    await downloadFile(downloadUrl, destPath, { quiet: config.quiet });

    // Pure local path output (stdout stays clean for piping)
    process.stdout.write(destPath);
    process.stdout.write('\n');
  },
});
