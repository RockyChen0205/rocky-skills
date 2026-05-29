import { defineCommand } from '../../command';
import { CLIError } from '../../errors/base';
import { ExitCode } from '../../errors/codes';
import { requestJson } from '../../client/http';
import { videoTaskEndpoint } from '../../client/endpoints';
import { formatOutput, detectOutputFormat } from '../../output/formatter';
import type { Config } from '../../config/schema';
import type { GlobalFlags } from '../../types/flags';
import type { VideoTaskResponse } from '../../types/api';

export default defineCommand({
  name: 'video task get',
  description: 'Query video task status',
  usage: 'mmx video task get --task-id <id>',
  options: [
    { flag: '--task-id <id>', description: 'Video generation task ID' },
  ],
  examples: [
    'mmx video task get --task-id 106916112212032',
    'mmx video task get --task-id 106916112212032 --output json',
  ],
  async run(config: Config, flags: GlobalFlags) {
    const taskId = flags.taskId as string | undefined;
    if (!taskId) {
      throw new CLIError(
        '--task-id is required.',
        ExitCode.USAGE,
        'mmx video task get --task-id <id>',
      );
    }

    if (config.dryRun) {
      console.log(`Would query task: ${taskId}`);
      return;
    }

    const url = videoTaskEndpoint(config.baseUrl, taskId);
    const response = await requestJson<VideoTaskResponse>(config, { url });
    const format = detectOutputFormat(config.output);

    if (config.quiet) {
      console.log(response.status);
      return;
    }

    console.log(formatOutput({
      task_id: response.task_id,
      status: response.status,
      file_id: response.file_id,
      video_width: response.video_width,
      video_height: response.video_height,
    }, format));
  },
});
