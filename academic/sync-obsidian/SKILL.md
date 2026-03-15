# SKILL.md

## sync-obsidian

**Description:** Automatically sync Claude Code session plans and implementation reports to your Obsidian vault — as Markdown notes + visual Canvas maps. Auto-detects project name.

**Argument hint:** `[plan|report] [title]`

**Allowed tools:** Read, Write, Bash, Glob, Grep, Edit

**Configuration:**

```
OBSIDIAN_VAULT = /Users/yu.chency/Documents/obsidian-repo/Academic
```

**Auto Project Detection (priority order):**

1. Git repo name: `basename $(git rev-parse --show-toplevel)`
2. Current directory name: `basename $PWD` (fallback)

**Usage:**

```
/sync-obsidian plan               # Sync the latest plan file
/sync-obsidian report             # Generate and sync an implementation report
/sync-obsidian plan Auth Redesign # Sync plan with custom title
/sync-obsidian report API Layer   # Sync report with custom title
```

**Output locations:**

- Markdown: `{OBSIDIAN_VAULT}/[Project] {project_name}/`
- Canvas: `{OBSIDIAN_VAULT}/[Project] {project_name}/canvas/`

**Key rules:**

- No YAML frontmatter — use `>` quote blocks for metadata
- Always output both files — Markdown + Canvas on every sync
- Report full paths — tell the user where both files were written
- Auto-create directories with `mkdir -p`
