# Format Adapters

## LaTeX

- Detect existing `\cite...{}` commands or bibliography declarations such as `\bibliography{}` and `\addbibresource{}`.
- Preserve the dominant command family when possible.
- If no recognizable citation style or bibliography target exists, do not write back automatically.

## Markdown

- Prefer Pandoc citations such as `[@key]` when a `bibliography:` field or existing citation markers are present.
- If the file has no recognizable citation syntax, fall back to suggestion mode.

## Typst

- Detect `#bibliography("file.bib")` or existing `@key` usage.
- Write back only when the bibliography target can be located safely.

## Bibliography Updates

- Avoid duplicate keys.
- Reuse an existing bibliography file when the paper already references one.
- If no bibliography file can be resolved, stop before writeback and keep the run in suggestion mode.

