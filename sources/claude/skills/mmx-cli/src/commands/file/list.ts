import { defineCommand } from '../../command';
import { requestJson } from '../../client/http';
import { fileListEndpoint } from '../../client/endpoints';
import { formatOutput, detectOutputFormat } from '../../output/formatter';
import type { Config } from '../../config/schema';
import type { GlobalFlags } from '../../types/flags';
import type { FileListResponse } from '../../types/api';

export default defineCommand({
  name: 'file list',
  description: 'List uploaded files in MiniMax storage',
  usage: 'mmx file list',
  examples: [
    'mmx file list',
    'mmx file list --output json',
  ],
  async run(config: Config, _flags: GlobalFlags) {
    const format = detectOutputFormat(config.output);

    if (config.dryRun) {
      process.stdout.write('Would list uploaded files.\n');
      return;
    }

    const url = fileListEndpoint(config.baseUrl);
    const response = await requestJson<FileListResponse>(config, { url, method: 'GET' });

    if (format !== 'text') {
      process.stdout.write(formatOutput(response, format) + '\n');
      return;
    }

    if (!response.data || response.data.length === 0) {
      process.stdout.write('No files found.\n');
      return;
    }

    const tableData = response.data.map((f) => ({
      ID: f.file_id,
      FILENAME: f.filename,
      PURPOSE: f.purpose,
      SIZE_KB: (f.bytes / 1024).toFixed(1),
      CREATED: new Date(f.created_at * 1000).toISOString().slice(0, 16).replace('T', ' '),
    }));

    const { formatTable } = await import('../../output/text');
    process.stdout.write(formatTable(tableData) + '\n');
  },
});
