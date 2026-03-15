#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict

from common import SOURCE_SCORES, generate_citation_key, normalize_text, read_json, write_json


def normalize_candidate(record: dict) -> dict:
    authors = record.get("authors") or []
    claim_text = record.get("claim_text", "")
    title = record.get("title", "")
    year = record.get("year")
    source = (record.get("source") or "").casefold()
    corroborating = record.get("corroborating_records") or []

    normalized_titles = {normalize_text(title)} if title else set()
    normalized_years = {str(year)} if year is not None else set()
    corroboration_sources = {source} if source else set()

    for item in corroborating:
        item_title = item.get("title")
        item_year = item.get("year")
        item_source = (item.get("source") or "").casefold()
        if item_title:
            normalized_titles.add(normalize_text(item_title))
        if item_year is not None:
            normalized_years.add(str(item_year))
        if item_source:
            corroboration_sources.add(item_source)

    reasons: list[str] = []
    status = "accepted"
    if not title:
        status = "rejected"
        reasons.append("missing-title")
    if not authors:
        status = "rejected"
        reasons.append("missing-authors")
    if year is None:
        status = "rejected"
        reasons.append("missing-year")
    has_identifier = bool(record.get("doi") or record.get("arxiv_id"))
    if len(normalized_titles) > 1:
        status = "rejected"
        reasons.append("title-conflict")
    if len(normalized_years) > 1:
        status = "rejected"
        reasons.append("year-conflict")
    if not has_identifier and len(corroboration_sources - {"google-scholar"}) < 2:
        status = "rejected"
        reasons.append("insufficient-corroboration")
    if source == "google-scholar" and not has_identifier and len(corroboration_sources) == 1:
        status = "rejected"
        reasons.append("scholar-only")

    confidence = SOURCE_SCORES.get(source, 1) + min(len(corroboration_sources), 3)
    citation_key = generate_citation_key(title, authors, year)
    overlap = 0.0
    abstract = normalize_text(record.get("abstract", ""))
    if claim_text and abstract:
        claim_terms = {term for term in normalize_text(claim_text).split(" ") if len(term) > 3}
        abstract_terms = {term for term in abstract.split(" ") if len(term) > 3}
        if claim_terms:
            overlap = len(claim_terms & abstract_terms) / len(claim_terms)

    normalized = dict(record)
    normalized.update(
        {
            "status": status,
            "reasons": reasons,
            "confidence": confidence,
            "citation_key": citation_key,
            "corroboration_sources": sorted(corroboration_sources),
            "semantic_overlap": round(overlap, 3),
        }
    )
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify citation metadata before placement or writeback.")
    parser.add_argument("claims_json")
    parser.add_argument("candidates_json")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    claims = {item["claim_id"]: item for item in read_json(args.claims_json)}
    candidates = read_json(args.candidates_json)

    verified: list[dict] = []
    by_claim: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        claim = claims.get(candidate.get("claim_id"))
        candidate["claim_text"] = claim["sentence"] if claim else ""
        normalized = normalize_candidate(candidate)
        verified.append(normalized)
        if claim:
            by_claim[claim["claim_id"]].append(normalized)

    summary = {
        "verified": verified,
        "counts": {
            "accepted": sum(1 for item in verified if item["status"] == "accepted"),
            "rejected": sum(1 for item in verified if item["status"] == "rejected"),
        },
        "by_claim": by_claim,
    }
    write_json(args.output, summary)
    print(f"verified {len(verified)} candidates -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

