#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict

from common import detect_format, load_text, read_json, render_marker, write_json


def choose_placements(paper: str, claims_json: str, verified_json: str, paragraph_cap: int, min_sentence_gap: int) -> dict:
    paper_text = load_text(paper)
    fmt = detect_format(paper, paper_text).name
    claims = read_json(claims_json)
    verified_blob = read_json(verified_json)
    verified_by_claim = verified_blob["by_claim"]

    paragraph_counts: dict[int, int] = defaultdict(int)
    last_sentence_by_paragraph: dict[int, int] = defaultdict(lambda: -999)
    recent_keys: dict[str, tuple[int, int]] = {}
    placements: list[dict] = []
    skipped: list[dict] = []

    for claim in claims:
        candidates = verified_by_claim.get(claim["claim_id"], [])
        accepted = [item for item in candidates if item["status"] == "accepted"]
        if not accepted:
            skipped.append({"claim_id": claim["claim_id"], "reason": "no-accepted-candidates"})
            continue
        paragraph_index = claim["paragraph_index"]
        sentence_index = claim["sentence_index"]
        if paragraph_counts[paragraph_index] >= paragraph_cap:
            skipped.append({"claim_id": claim["claim_id"], "reason": "paragraph-cap"})
            continue
        if sentence_index - last_sentence_by_paragraph[paragraph_index] <= min_sentence_gap:
            skipped.append({"claim_id": claim["claim_id"], "reason": "sentence-gap"})
            continue

        accepted.sort(key=lambda item: (item["confidence"], item["semantic_overlap"]), reverse=True)
        chosen = None
        for candidate in accepted:
            recent = recent_keys.get(candidate["citation_key"])
            if recent and abs(paragraph_index - recent[0]) <= 1:
                continue
            chosen = candidate
            break
        if not chosen:
            skipped.append({"claim_id": claim["claim_id"], "reason": "recent-reuse"})
            continue

        placements.append(
            {
                "claim_id": claim["claim_id"],
                "paragraph_index": paragraph_index,
                "sentence_index": sentence_index,
                "sentence": claim["sentence"],
                "format": fmt,
                "citation_key": chosen["citation_key"],
                "citation_marker": render_marker(fmt, chosen["citation_key"]),
                "candidate": chosen,
            }
        )
        paragraph_counts[paragraph_index] += 1
        last_sentence_by_paragraph[paragraph_index] = sentence_index
        recent_keys[chosen["citation_key"]] = (paragraph_index, sentence_index)

    return {"placements": placements, "skipped": skipped, "format": fmt}


def main() -> int:
    parser = argparse.ArgumentParser(description="Choose dispersed citation placements.")
    parser.add_argument("paper")
    parser.add_argument("claims_json")
    parser.add_argument("verified_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--paragraph-cap", type=int, default=2)
    parser.add_argument("--min-sentence-gap", type=int, default=1)
    args = parser.parse_args()

    payload = choose_placements(args.paper, args.claims_json, args.verified_json, args.paragraph_cap, args.min_sentence_gap)
    write_json(args.output, payload)
    print(f"selected {len(payload['placements'])} placements -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

