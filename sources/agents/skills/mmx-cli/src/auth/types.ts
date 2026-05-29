export type AuthMethod = 'api-key' | 'oauth';

export interface OAuthTokens {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: 'Bearer';
}

export interface CredentialFile {
  access_token: string;
  refresh_token: string;
  expires_at: string; // ISO 8601
  token_type: 'Bearer';
  account?: string;
}

export interface ResolvedCredential {
  token: string;
  method: AuthMethod;
  source: string;
}
