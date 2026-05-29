import { describe, it, expect } from 'bun:test';
import { ensureFreshToken } from '../../src/auth/refresh';
import type { CredentialFile } from '../../src/auth/types';

describe('ensureFreshToken', () => {
  it('returns existing token when not expired', async () => {
    const creds: CredentialFile = {
      access_token: 'valid-token',
      refresh_token: 'refresh-token',
      expires_at: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
      token_type: 'Bearer',
    };

    const token = await ensureFreshToken(creds);
    expect(token).toBe('valid-token');
  });
});
