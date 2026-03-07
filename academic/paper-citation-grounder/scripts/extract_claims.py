#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import claim_score, detect_format, load_text, split_paragraphs, split_sentences, write_json


def build_claims(path: str, min_score: int) -> list[dict]:
    content = load_text(path)
    fmt = detect_format(path, content).name
    claims: list[dict] = []
    claim_index = 1
    for paragraph_index, paragraph in enumerate(split_paragraphs(content)):
        sentences = split_sentences(paragraph)
        for sentence_index, sentence in enumerate(sentences):
            score, reasons = claim_score(sentence, fmt)
            if score < min_score:
                continue
            claims.append(
                {
                    "claim_id": f"claim-{claim_index:04d}",
                    "paper_path": str(Path(path).resolve()),
                    "format": fmt,
                    "paragraph_index": paragraph_index,
                    "sentence_index": sentence_index,
                    "sentence": sentence,
                    "claim_score": score,
                    "claim_reasons": reasons,
                }
            )
            claim_index += 1
    return claims


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract likely citation-worthy claims from a paper.")
    parser.add_argument("paper")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--min-score", type=int, default=3)
    args = parser.parse_args()

    claims = build_claims(args.paper, args.min_score)
    write_json(args.output, claims)
    print(f"extracted {len(claims)} claims -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

