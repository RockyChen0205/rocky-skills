import { describe, it, expect } from 'bun:test';
import { mapApiError } from '../../src/errors/api';
import { ExitCode } from '../../src/errors/codes';

describe('mapApiError', () => {
  it('maps 401 to AUTH exit code', () => {
    const err = mapApiError(401, {});
    expect(err.exitCode).toBe(ExitCode.AUTH);
    expect(err.message).toContain('401');
  });

  it('maps 403 to AUTH exit code', () => {
    const err = mapApiError(403, {});
    expect(err.exitCode).toBe(ExitCode.AUTH);
  });

  it('maps 429 to QUOTA exit code', () => {
    const err = mapApiError(429, { base_resp: { status_code: 0, status_msg: 'rate limited' } });
    expect(err.exitCode).toBe(ExitCode.QUOTA);
  });

  it('maps 408 to TIMEOUT exit code', () => {
    const err = mapApiError(408, {});
    expect(err.exitCode).toBe(ExitCode.TIMEOUT);
  });

  it('maps MiniMax content filter code 1002', () => {
    const err = mapApiError(400, { base_resp: { status_code: 1002, status_msg: 'content filtered' } });
    expect(err.exitCode).toBe(ExitCode.CONTENT_FILTER);
  });

  it('maps MiniMax quota code 1028', () => {
    const err = mapApiError(400, { base_resp: { status_code: 1028, status_msg: 'quota exhausted' } });
    expect(err.exitCode).toBe(ExitCode.QUOTA);
  });

  it('maps unknown errors to GENERAL', () => {
    const err = mapApiError(500, { base_resp: { status_code: 0, status_msg: 'internal error' } });
    expect(err.exitCode).toBe(ExitCode.GENERAL);
  });

  it('includes API message in error', () => {
    const err = mapApiError(500, { base_resp: { status_code: 0, status_msg: 'something broke' } });
    expect(err.message).toContain('something broke');
  });
});
