import { REGIONS, type Region } from './schema';
import { readConfigFile, writeConfigFile } from './loader';

const QUOTA_PATH = '/v1/api/openplatform/coding_plan/remains';

function quotaUrl(region: Region): string {
  return REGIONS[region] + QUOTA_PATH;
}

async function probeRegion(region: Region, apiKey: string, timeoutMs: number): Promise<boolean> {
  try {
    const res = await fetch(quotaUrl(region), {
      headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(timeoutMs),
    });
    if (!res.ok) return false;
    const data = await res.json() as { base_resp?: { status_code?: number } };
    return data.base_resp?.status_code === 0;
  } catch {
    return false;
  }
}

export async function detectRegion(apiKey: string): Promise<Region> {
  process.stderr.write('Detecting region...');
  const regions = Object.keys(REGIONS) as Region[];
  const results = await Promise.all(
    regions.map(async (r) => ({ region: r, ok: await probeRegion(r, apiKey, 5000) })),
  );
  const match = results.find((r) => r.ok);
  if (!match) {
    process.stderr.write(' failed\n');
    process.stderr.write('Warning: API key failed validation against all regions. Falling back to global.\n');
    return 'global';
  }
  const detected: Region = match.region;
  process.stderr.write(` ${detected}\n`);
  return detected;
}

export async function saveDetectedRegion(region: Region): Promise<void> {
  const existing = readConfigFile() as Record<string, unknown>;
  existing.region = region;
  await writeConfigFile(existing);
}
