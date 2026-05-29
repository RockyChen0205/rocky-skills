/**
 * Interactive prompt utilities.
 *
 * Wraps @clack/prompts with environment-awareness:
 * - In interactive mode: shows prompts and lets users input values.
 * - In non-interactive / CI / Agent mode: fails fast with a clear error.
 *
 * All functions here are no-ops (return undefined) when non-interactive,
 * so callers must check isInteractive() first or handle the missing-value
 * case explicitly.
 */

import { isInteractive } from './env.js';
import { CLIError } from '../errors/base.js';
import { ExitCode } from '../errors/codes';

// Dynamic import to avoid loading @clack/prompts in non-interactive envs unnecessarily
// (though for CLI tools the startup cost is usually acceptable)

/**
 * Prompt the user for a text value.
 * Only call this when isInteractive() is true; otherwise the function returns
 * undefined immediately so the caller can fail fast.
 */
export async function promptText(options: {
  message: string;
  defaultValue?: string;
}): Promise<string | undefined> {
  if (!isInteractive()) return undefined;

  const { defaultValue, message } = options;
  const inquirer = await import('@clack/prompts');
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const val = await (inquirer as any).text({
    message,
    default: defaultValue,
    placeholder: defaultValue,
  });

  // @clack/prompts returns a Symbol.cancel when the user presses Ctrl+C
  if (typeof val === 'symbol') return undefined;
  return val as string;
}

/**
 * Like promptText but confirms with y/N before proceeding.
 */
export async function promptConfirm(options: {
  message: string;
}): Promise<boolean | undefined> {
  if (!isInteractive()) return undefined;

  const { message } = options;
  const inquirer = await import('@clack/prompts');
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const val = await (inquirer as any).confirm({ message });

  if (typeof val === 'symbol') return undefined;
  return val as boolean;
}

/**
 * Fail fast with a user-friendly error when a required option is missing
 * in non-interactive (agent / CI) mode.
 */
export function failIfMissing(flagName: string, context: string): never {
  throw new CLIError(
    `Missing required argument: --${flagName}\n` +
    `Hint: In non-interactive (CI / agent) environments all required flags must be provided.\n` +
    `      In an interactive terminal, run without --${flagName} and the CLI will prompt for it.`,
    ExitCode.USAGE,
    context,
  );
}
