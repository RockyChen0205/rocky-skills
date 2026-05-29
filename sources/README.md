# Synced Local Skills

This directory mirrors local skill directories from the home-level agent
configuration folders.

## Sources

- `agents/skills/` mirrors `~/.agents/skills/`
- `codex/skills/` mirrors `~/.codex/skills/`
- `codex/vendor_imports/skills/` mirrors `~/.codex/vendor_imports/skills/`
- `claude/skills/` mirrors `~/.claude/skills/`

## Exclusions

The sync intentionally excludes local/generated metadata that should not be
published in a public repository:

- `.git/`
- `.venv/`
- `node_modules/`
- `__pycache__/`
- `.DS_Store`

