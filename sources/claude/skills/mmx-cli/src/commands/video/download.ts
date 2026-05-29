import { defineCommand } from '../../command';
import { CLIError } from '../../errors/base';
import { ExitCode } from '../../errors/codes';
import { requestJson } from '../../client/http';
import { fileRetrieveEndpoint } from '../../client/endpoints';
import { downloadFile, formatBytes } from '../../files/download';
import { formatOutput, detectOutputFormat } from '../../output/formatter';
import type { Config } from '../../config/schema';
import type { GlobalFlags } from '../../types/flags';
import type { FileRetrieveResponse } from '../../types/api';

export default defineCommand({
  name: 'video download',
  description: 'Download a completed video by file ID',
  usage: 'mmx video download --file-id <id> --out <path>',
  options: [
    { flag: '--file-id <id>', description: 'File ID to download' },
    { flag: '--out <path>', description: 'Output file path' },
  ],
  examples: [
    'mmx video download --file-id 176844028768320 --out video.mp4',
    'mmx video download --file-id 176844028768320 --out video.mp4 --quiet',
  ],
  async run(config: Config, flags: GlobalFlags) {
    const fileId = flags.fileId as string | undefined;
    if (!fileId) {
      throw new CLIError(
        '--file-id is required.',
        ExitCode.USAGE,
        'mmx video download --file-id <id> --out <path>',
      );
    }

    const outPath = flags.out as string | undefined;
    if (!outPath) {
      throw new CLIError(
        '--out is required.',
        ExitCode.USAGE,
        'mmx video download --file-id <id> --out video.mp4',
      );
    }

    if (config.dryRun) {
      console.log(`Would download file ${fileId} to ${outPath}`);
      return;
    }

    // Get file info to find download URL
    const url = fileRetrieveEndpoint(config.baseUrl, fileId);
    const fileInfo = await requestJson<FileRetrieveResponse>(config, { url });

    const downloadUrl = fileInfo.file?.download_url;
    if (!downloadUrl) {
      throw new CLIError(
        'No download URL available for this file.',
        ExitCode.GENERAL,
        'The file may still be processing. Check task status first.',
      );
    }

    const { size } = await downloadFile(downloadUrl, outPath, { quiet: config.quiet });
    const format = detectOutputFormat(config.output);

    if (config.quiet) {
      console.log(outPath);
      return;
    }

    console.log(formatOutput({
      saved: outPath,
      size: formatBytes(size),
    }, format));
  },
});
