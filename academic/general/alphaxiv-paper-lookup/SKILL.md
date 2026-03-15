---
name: alphaxiv-paper-lookup
description: Look up arXiv papers on alphaxiv.org to get structured AI-generated overviews, faster and more reliable than reading raw PDFs
---

# AlphaXiv Paper Lookup

This skill provides access to AlphaXiv, a service that generates AI-powered structured overviews of arXiv papers.

## When to Use This Skill

Use this skill when:
- User shares an arXiv URL (e.g., `arxiv.org/abs/2401.12345`)
- User mentions a paper ID (e.g., `2401.12345`)
- User asks to explain, summarize, or analyze a research paper
- User shares an AlphaXiv URL

## How to Use

This skill fetches machine-readable reports from AlphaXiv. No additional scripts or dependencies required.

### Basic Usage

**Step 1: Extract the paper ID** from the input (URLs, IDs with or without version)

**Step 2: Fetch the AI-generated overview**
```bash
curl -s "https://alphaxiv.org/overview/{PAPER_ID}.md"
```

This returns structured markdown analysis optimized for LLMs.

**Step 3 (Fallback): If more detail is needed**
```bash
curl -s "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

This fetches the full paper text.

### Examples

Get overview for a paper:
```bash
curl -s "https://alphaxiv.org/overview/2401.12345.md"
```

Get full text:
```bash
curl -s "https://alphaxiv.org/abs/2401.12345.md"
```

### Supported Input Formats

- Full URL: `https://arxiv.org/abs/2401.12345`
- With version: `arxiv.org/abs/2401.12345v1`
- Paper ID only: `2401.12345`

## Output Format

Returns structured Markdown content including:
- Paper title and authors
- Abstract summary
- Key contributions
- Method overview
- Technical details

All formatted for easy LLM consumption and understanding.

## Error Handling

| Error | Meaning |
|-------|---------|
| 404 on overview endpoint | Report not generated yet |
| 404 on full text endpoint | Full text not processed yet |

If both fail, direct user to the original PDF as last resort.

## Notes

- **No authentication required** - Public endpoints
- **No API key needed** - Free to use
- **Faster than reading PDFs** - AI-generated summaries save time
- **Optimized for LLMs** - Structured output format
