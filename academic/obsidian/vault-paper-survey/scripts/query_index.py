#!/usr/bin/env python3
"""Query paper-index.yaml files with simple scoring."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def load_items(index_path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []
    items: list[dict[str, Any]] = []
    for raw in data:
        if not isinstance(raw, dict):
            continue
        record = dict(raw)
        record["_index_path"] = str(index_path)
        record["_directory"] = str(index_path.parent)
        items.append(record)
    return items


def collect_items(root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for index_path in sorted(root.rglob("paper-index.yaml")):
        items.extend(load_items(index_path))
    return items


def matches_text(needle: str, *fields: str) -> bool:
    target = " ".join(normalize(field) for field in fields if field)
    return normalize(needle) in target


def compute_score(
    item: dict[str, Any],
    keywords: list[str],
    tasks: list[str],
    methods: list[str],
    highlights: list[str],
    team_terms: list[str],
    dir_terms: list[str],
) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0

    title = str(item.get("title", ""))
    contrib = str(item.get("core_contribution", ""))
    directory = str(item.get("_directory", ""))
    team = str(item.get("team", ""))
    task_values = ensure_list(item.get("task_type"))
    method_values = ensure_list(item.get("method_type"))
    highlight_values = ensure_list(item.get("tech_highlights"))

    for keyword in keywords:
        if matches_text(keyword, title, contrib, directory, str(item.get("id", ""))):
            score += 2
            reasons.append(f"keyword:{keyword}")

    for task in tasks:
        if any(normalize(task) == normalize(value) for value in task_values):
            score += 4
            reasons.append(f"task:{task}")

    for method in methods:
        if any(normalize(method) == normalize(value) for value in method_values):
            score += 4
            reasons.append(f"method:{method}")

    for highlight in highlights:
        if any(normalize(highlight) == normalize(value) for value in highlight_values):
            score += 3
            reasons.append(f"highlight:{highlight}")

    for team_term in team_terms:
        if matches_text(team_term, team):
            score += 2
            reasons.append(f"team:{team_term}")

    for dir_term in dir_terms:
        if matches_text(dir_term, directory):
            score += 3
            reasons.append(f"dir:{dir_term}")

    return score, reasons


def resolve_note_path(item: dict[str, Any]) -> str | None:
    note_path = item.get("note_path")
    if note_path:
        return str(Path(str(item["_directory"])) / str(note_path))
    inferred = Path(str(item["_directory"])) / f"{item.get('id', '')}.md"
    return str(inferred)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="03-Papers")
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--task", action="append", default=[])
    parser.add_argument("--method", action="append", default=[])
    parser.add_argument("--highlight", action="append", default=[])
    parser.add_argument("--team", action="append", default=[])
    parser.add_argument("--dir", dest="dirs", action="append", default=[])
    parser.add_argument("--year-min", type=int)
    parser.add_argument("--year-max", type=int)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--format", choices=["json", "table", "markdown"], default="json")
    return parser.parse_args()


def format_table(rows: list[dict[str, Any]], root: Path) -> str:
    headers = ["score", "year", "title", "directory", "task_type", "method_type"]
    lines = ["\t".join(headers)]
    for row in rows:
        lines.append(
            "\t".join(
                [
                    str(row["score"]),
                    str(row.get("year", "")),
                    str(row.get("title", "")),
                    str(Path(row["_directory"]).resolve().relative_to(root.parent.resolve())),
                    ",".join(ensure_list(row.get("task_type"))[:4]),
                    ",".join(ensure_list(row.get("method_type"))[:4]),
                ]
            )
        )
    return "\n".join(lines)


def format_markdown(rows: list[dict[str, Any]], root: Path) -> str:
    lines = []
    for row in rows:
        rel_dir = Path(row["_directory"]).resolve().relative_to(root.parent.resolve())
        lines.append(f"- [{row['score']}] {row.get('title', '')}")
        lines.append(f"  - dir: {rel_dir}")
        lines.append(f"  - year: {row.get('year', '')}")
        lines.append(f"  - task: {', '.join(ensure_list(row.get('task_type')))}")
        lines.append(f"  - method: {', '.join(ensure_list(row.get('method_type')))}")
        lines.append(f"  - reasons: {', '.join(row['match_reasons'])}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Root not found: {root}")

    rows = []
    for item in collect_items(root):
        year = item.get("year")
        if args.year_min is not None and isinstance(year, int) and year < args.year_min:
            continue
        if args.year_max is not None and isinstance(year, int) and year > args.year_max:
            continue

        score, reasons = compute_score(
            item,
            keywords=args.keyword,
            tasks=args.task,
            methods=args.method,
            highlights=args.highlight,
            team_terms=args.team,
            dir_terms=args.dirs,
        )
        if score <= 0 and any([args.keyword, args.task, args.method, args.highlight, args.team, args.dirs]):
            continue
        item["score"] = score
        item["match_reasons"] = reasons
        item["resolved_note_path"] = resolve_note_path(item)
        rows.append(item)

    rows.sort(key=lambda row: (row["score"], row.get("year", 0)), reverse=True)
    rows = rows[: args.limit]

    if args.format == "table":
        print(format_table(rows, root))
    elif args.format == "markdown":
        print(format_markdown(rows, root))
    else:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
