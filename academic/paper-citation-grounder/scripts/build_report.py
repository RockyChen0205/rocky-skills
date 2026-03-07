#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import read_json, write_json


def build_markdown(claims: list[dict], verified: dict, placements: dict) -> str:
    lines = [
        "# Citation Grounding Report",
        "",
        f"- Claims extracted: {len(claims)}",
        f"- Accepted candidates: {verified['counts']['accepted']}",
        f"- Rejected candidates: {verified['counts']['rejected']}",
        f"- Placements selected: {len(placements['placements'])}",
        f"- Placements skipped: {len(placements['skipped'])}",
        "",
        "## Accepted Placements",
        "",
    ]
    if not placements["placements"]:
        lines.append("No placements were selected.")
    for placement in placements["placements"]:
        candidate = placement["candidate"]
        lines.extend(
            [
                f"### {placement['claim_id']}",
                f"- Sentence: {placement['sentence']}",
                f"- Citation key: `{placement['citation_key']}`",
                f"- Title: {candidate['title']}",
                f"- Source: {candidate['source']}",
                f"- Confidence: {candidate['confidence']}",
                f"- Corroboration: {', '.join(candidate['corroboration_sources'])}",
                f"- DOI: {candidate.get('doi') or 'n/a'}",
                f"- arXiv: {candidate.get('arxiv_id') or 'n/a'}",
                "",
            ]
        )
    lines.extend(["## Skips", ""])
    for item in placements["skipped"]:
        lines.append(f"- {item['claim_id']}: {item['reason']}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build JSON and Markdown citation-grounding reports.")
    parser.add_argument("claims_json")
    parser.add_argument("verified_json")
    parser.add_argument("placements_json")
    parser.add_argument("-o", "--output-prefix", required=True)
    args = parser.parse_args()

    claims = read_json(args.claims_json)
    verified = read_json(args.verified_json)
    placements = read_json(args.placements_json)

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix(".json")
    md_path = prefix.with_suffix(".md")

    payload = {"claims": claims, "verified": verified, "placements": placements}
    write_json(json_path, payload)
    md_path.write_text(build_markdown(claims, verified, placements), encoding="utf-8")
    print(f"wrote report -> {json_path}, {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

