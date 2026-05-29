import { describe, it, expect, beforeEach, afterEach } from 'bun:test';
import { saveCredentials, loadCredentials, clearCredentials } from '../../src/auth/credentials';
import type { CredentialFile } from '../../src/auth/types';
import { mkdirSync, rmSync, existsSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

describe('credentials', () => {
  const testDir = join(tmpdir(), `mmx-test-${Date.now()}`);
  const originalHome = process.env.HOME;

  beforeEach(() => {
    mkdirSync(join(testDir, '.mmx'), { recursive: true });
    process.env.HOME = testDir;
  });

  afterEach(() => {
    process.env.HOME = originalHome;
    if (existsSync(testDir)) {
      rmSync(testDir, { recursive: true, force: true });
    }
  });

  it('returns null when no credentials file exists', async () => {
    const creds = await loadCredentials();
    expect(creds).toBeNull();
  });

  it('saves and loads credentials', async () => {
    const creds: CredentialFile = {
      access_token: 'test-access-token',
      refresh_token: 'test-refresh-token',
      expires_at: new Date(Date.now() + 3600000).toISOString(),
      token_type: 'Bearer',
      account: 'test@example.com',
    };

    await saveCredentials(creds);
    const loaded = await loadCredentials();

    expect(loaded).not.toBeNull();
    expect(loaded!.access_token).toBe('test-access-token');
    expect(loaded!.refresh_token).toBe('test-refresh-token');
    expect(loaded!.account).toBe('test@example.com');
  });

  it('clears credentials', async () => {
    const creds: CredentialFile = {
      access_token: 'test',
      refresh_token: 'test',
      expires_at: new Date().toISOString(),
      token_type: 'Bearer',
    };

    await saveCredentials(creds);
    await clearCredentials();
    const loaded = await loadCredentials();
    expect(loaded).toBeNull();
  });
});
