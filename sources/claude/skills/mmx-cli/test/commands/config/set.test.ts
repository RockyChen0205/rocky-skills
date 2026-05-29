import { describe, it, expect } from 'bun:test';
import { default as setCommand } from '../../../src/commands/config/set';

describe('config set command', () => {
  it('has correct name', () => {
    expect(setCommand.name).toBe('config set');
  });

  it('requires key and value', async () => {
    const config = {
      region: 'global' as const,
      baseUrl: 'https://api.mmx.io',
      output: 'text' as const,
      timeout: 10,
      verbose: false,
      quiet: false,
      noColor: true,
      yes: false,
      dryRun: false,
      nonInteractive: true,
      async: false,
    };

    await expect(
      setCommand.execute(config, {
        quiet: false,
        verbose: false,
        noColor: true,
        yes: false,
        dryRun: false,
        help: false,
        nonInteractive: true,
        async: false,
      }),
    ).rejects.toThrow('--key and --value are required');
  });

  it('validates config key', async () => {
    const config = {
      region: 'global' as const,
      baseUrl: 'https://api.mmx.io',
      output: 'text' as const,
      timeout: 10,
      verbose: false,
      quiet: false,
      noColor: true,
      yes: false,
      dryRun: false,
      nonInteractive: true,
      async: false,
    };

    await expect(
      setCommand.execute(config, {
        key: 'invalid_key',
        value: 'test',
        quiet: false,
        verbose: false,
        noColor: true,
        yes: false,
        dryRun: false,
        help: false,
        nonInteractive: true,
        async: false,
      }),
    ).rejects.toThrow('Invalid config key');
  });
});
