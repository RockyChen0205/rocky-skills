import { defineCommand } from '../../command';
import { registry } from '../../registry';
import { generateToolSchema } from '../../utils/schema';
import type { Config } from '../../config/schema';
import type { GlobalFlags } from '../../types/flags';
import { CLIError } from '../../errors/base';
import { ExitCode } from '../../errors/codes';

/**
 * Commands that are infrastructure/auth-related and not suitable as Agent tools.
 */
const SKIP_PREFIXES = ['auth ', 'config ', 'update'];

export default defineCommand({
  name: 'config export-schema',
  description:
    'Export all (or one) CLI command(s) as Anthropic/OpenAI-compatible JSON tool schemas',
  usage: 'mmx config export-schema [--command "<name>"]',
  options: [
    {
      flag: '--command <name>',
      description:
        'Export schema for a specific command only (e.g. "image generate")',
    },
  ],
  examples: [
    'mmx config export-schema',
    'mmx config export-schema --command "video generate"',
  ],
  async run(config: Config, flags: GlobalFlags) {
    const targetCommand = flags.command as string | undefined;

    if (targetCommand) {
      try {
        const { command } = registry.resolve(targetCommand.split(' '));
        const schema = generateToolSchema(command);
        process.stdout.write(JSON.stringify(schema, null, 2) + '\n');
      } catch {
        throw new CLIError(
          `Command "${targetCommand}" not found.`,
          ExitCode.USAGE,
        );
      }
      return;
    }

    // Export all suitable commands
    const allCommands = registry.getAllCommands();
    const schemas = allCommands
      .filter((c) => !SKIP_PREFIXES.some((p) => c.name.startsWith(p)))
      .map((c) => generateToolSchema(c));

    process.stdout.write(JSON.stringify(schemas, null, 2) + '\n');
  },
});
