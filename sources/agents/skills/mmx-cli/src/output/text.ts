export function formatText(data: unknown): string {
  if (data === null || data === undefined) return '';
  if (typeof data === 'string') return data;
  if (typeof data === 'number' || typeof data === 'boolean') return String(data);

  if (Array.isArray(data)) {
    if (data.length === 0) return '(empty)';
    if (typeof data[0] === 'object' && data[0] !== null) {
      return formatTable(data as Record<string, unknown>[]);
    }
    return data.map(String).join('\n');
  }

  if (typeof data === 'object') {
    return formatKeyValue(data as Record<string, unknown>);
  }

  return String(data);
}

export function formatKeyValue(obj: Record<string, unknown>, indent = 0): string {
  const prefix = ' '.repeat(indent);
  const lines: string[] = [];

  for (const [key, value] of Object.entries(obj)) {
    if (value === null || value === undefined) continue;
    if (Array.isArray(value)) {
      lines.push(`${prefix}${key}:`);
      for (const item of value) {
        if (typeof item === 'object' && item !== null) {
          lines.push(`${prefix}  - ${formatKeyValue(item as Record<string, unknown>, indent + 4).trimStart()}`);
        } else {
          lines.push(`${prefix}  - ${String(item)}`);
        }
      }
    } else if (typeof value === 'object') {
      lines.push(`${prefix}${key}:`);
      lines.push(formatKeyValue(value as Record<string, unknown>, indent + 2));
    } else {
      lines.push(`${prefix}${key}: ${String(value)}`);
    }
  }

  return lines.join('\n');
}

export function formatTable(rows: Record<string, unknown>[]): string {
  if (rows.length === 0) return '(empty)';

  const keys = Object.keys(rows[0]!);
  const widths = keys.map(k =>
    Math.max(k.length, ...rows.map(r => String(r[k] ?? '').length)),
  );

  const header = keys.map((k, i) => k.toUpperCase().padEnd(widths[i]!)).join('  ');
  const separator = widths.map(w => '-'.repeat(w)).join('  ');
  const body = rows.map(r =>
    keys.map((k, i) => String(r[k] ?? '').padEnd(widths[i]!)).join('  '),
  );

  return [header, separator, ...body].join('\n');
}
