#!/usr/bin/env python3
"""Discover paper-index.yaml files under a root directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> list[dict[str, Any]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def summarize_index(path: Path, root: Path) -> dict[str, Any]:
    items = load_yaml(path)
    years = sorted({item.get("year") for item in items if item.get("year") is not None})
    task_types = sorted(
        {
            tag
            for item in items
            for tag in (item.get("task_type") or [])
            if isinstance(tag, str)
        }
    )
    method_types = sorted(
        {
            tag
            for item in items
            for tag in (item.get("method_type") or [])
            if isinstance(tag, str)
        }
    )
    return {
        "index_path": str(path.relative_to(root.parent if root.name else root)),
        "directory": str(path.parent.relative_to(root.parent if root.name else root)),
        "paper_count": len(items),
        "years": years,
        "task_types": task_types,
        "method_types": method_types,
    }


def format_table(rows: list[dict[str, Any]]) -> str:
    headers = ["directory", "paper_count", "years", "task_types"]
    table = ["\t".join(headers)]
    for row in rows:
        table.append(
            "\t".join(
                [
                    row["directory"],
                    str(row["paper_count"]),
                    ",".join(str(year) for year in row["years"]),
                    ",".join(row["task_types"][:8]),
                ]
            )
        )
    return "\n".join(table)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default="03-Papers")
    parser.add_argument("--format", choices=["json", "table"], default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Root not found: {root}")

    rows = [
        summarize_index(path, root)
        for path in sorted(root.rglob("paper-index.yaml"))
    ]

    if args.format == "table":
        print(format_table(rows))
    else:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
