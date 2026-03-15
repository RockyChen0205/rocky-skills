---
name: paper-citation-grounder
description: Find, verify, and insert trustworthy academic citations into a paper while avoiding fabricated references and citation clustering. Use when Codex needs to read a paper draft, identify unsupported claims, search Google Scholar and arXiv for relevant literature, cross-check metadata with authoritative sources, suggest citation placements, or write back dispersed citations into LaTeX, Markdown, or Typst sources.
---

# Paper Citation Grounder

Read the paper source first. Prefer full-document runs over isolated sentences so placement decisions can stay dispersed across the draft instead of clustering at paragraph ends.

## Workflow

1. Parse the paper and extract candidate claims with `scripts/extract_claims.py`.
2. Generate search tasks with `scripts/search_candidates.py`, then search `Google Scholar` and `arXiv` for each claim. Use `agent-reach`, `url-reader`, or the built-in web tool to gather candidate metadata. Save candidates as JSON before writeback.
3. Verify every candidate with `scripts/verify_metadata.py`. Reject anything without stable identifiers or independent corroboration.
4. Choose sentence-level placements with `scripts/place_citations.py`. Respect paragraph density limits and reuse suppression.
5. In `suggest` mode, stop after generating the report with `scripts/build_report.py`.
6. In `writeback` mode, only proceed if the paper already has a recognizable citation style. Then run `scripts/writeback_citations.py`.

## Operating Rules

- Reject unverified references. Do not “fill in” missing title, author, or year from intuition.
- Prefer no citation over a weak citation. If verification fails, report the gap and skip insertion.
- Treat `Google Scholar` as a discovery surface, not a final source of truth.
- Favor candidates with `DOI` or `arXiv ID`. If neither exists, require corroborating metadata from at least two authoritative sources.
- Keep citations dispersed. The goal is support at the claim site, not a pile of references at the end of a paragraph.
- Preserve the paper’s current citation style. If no style can be detected safely, fall back to `suggest` mode.

## Required Candidate Schema

Candidate JSON is a list of objects. Each object must include:

```json
{
  "claim_id": "claim-0001",
  "source": "google-scholar",
  "title": "Paper title",
  "authors": ["First Author", "Second Author"],
  "year": 2024,
  "venue": "Conference or Journal",
  "doi": "10.1000/example",
  "arxiv_id": null,
  "url": "https://...",
  "abstract": "Optional abstract",
  "query": "original search query",
  "corroborating_records": [
    {
      "source": "crossref",
      "title": "Paper title",
      "authors": ["First Author", "Second Author"],
      "year": 2024,
      "doi": "10.1000/example",
      "arxiv_id": null
    }
  ]
}
```

Use `references/verification-rules.md` for acceptance criteria and `references/source-priority.md` for source trust ordering.

## Commands

Run the full local pipeline:

```bash
python3 scripts/pipeline.py path/to/paper.tex \
  --candidates path/to/candidates.json \
  --mode suggest \
  --output-dir out/
```

Write back verified citations:

```bash
python3 scripts/pipeline.py path/to/paper.tex \
  --candidates path/to/candidates.json \
  --mode writeback \
  --output-dir out/
```

Run the steps independently when debugging:

```bash
python3 scripts/extract_claims.py paper.tex -o claims.json
python3 scripts/search_candidates.py claims.json -o search_tasks.json
python3 scripts/verify_metadata.py claims.json candidates.json -o verified.json
python3 scripts/place_citations.py paper.tex claims.json verified.json -o placements.json
python3 scripts/writeback_citations.py paper.tex placements.json --output out/paper.tex
python3 scripts/build_report.py claims.json verified.json placements.json -o out/report
```

## Resources

- `references/source-priority.md`: trust ordering and fallback policy for Scholar, arXiv, Crossref, OpenAlex, and Semantic Scholar.
- `references/placement-rules.md`: sentence-level placement and clustering suppression rules.
- `references/verification-rules.md`: minimum metadata checks and rejection criteria.
- `references/format-adapters.md`: writeback constraints for LaTeX, Markdown, and Typst.
- `scripts/search_candidates.py`: turn extracted claims into search-ready Scholar and arXiv query tasks.
- `scripts/pipeline.py`: end-to-end orchestration for local runs.
