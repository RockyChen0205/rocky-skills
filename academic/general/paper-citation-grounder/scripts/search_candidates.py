#!/usr/bin/env python3
from __future__ import annotations

import argparse

from common import normalize_text, read_json, write_json


STOPWORDS = {
    "the",
    "and",
    "that",
    "with",
    "from",
    "this",
    "into",
    "their",
    "there",
    "about",
    "which",
    "while",
    "using",
    "paper",
    "method",
    "results",
    "recent",
    "prior",
    "work",
    "studies",
    "shows",
    "suggests",
}


def build_query(sentence: str, max_terms: int) -> str:
    terms = []
    for token in normalize_text(sentence).split(" "):
        if len(token) < 4 or token in STOPWORDS or token.isdigit():
            continue
        if token not in terms:
            terms.append(token)
        if len(terms) >= max_terms:
            break
    return " ".join(terms)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Scholar/arXiv search tasks from extracted claims.")
    parser.add_argument("claims_json")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--max-terms", type=int, default=8)
    args = parser.parse_args()

    claims = read_json(args.claims_json)
    tasks = []
    for claim in claims:
        query = build_query(claim["sentence"], args.max_terms)
        tasks.append(
            {
                "claim_id": claim["claim_id"],
                "sentence": claim["sentence"],
                "priority": claim["claim_score"],
                "queries": {
                    "google_scholar": query,
                    "arxiv": query,
                },
                "instructions": "Search Scholar for recall, then verify metadata against arXiv, Crossref, OpenAlex, or Semantic Scholar before acceptance.",
            }
        )

    write_json(args.output, tasks)
    print(f"generated {len(tasks)} search tasks -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
