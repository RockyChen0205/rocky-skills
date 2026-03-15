#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import bibtex_entry, detect_format, insert_before_terminal_punctuation, load_text, read_json


def detect_style(fmt: str, content: str) -> tuple[str | None, Path | None]:
    if fmt == "latex":
        commands = re.findall(r"(\\cite\w*)\{[^}]+\}", content)
        command = commands[0] if commands else None
        bib_match = re.search(r"\\(?:bibliography|addbibresource)\{([^}]+)\}", content)
        bib_target = None
        if bib_match:
            raw_target = bib_match.group(1).split(",")[0].strip()
            if not raw_target.endswith(".bib"):
                raw_target += ".bib"
            bib_target = Path(raw_target)
        if command or bib_target:
            return command or "\\cite", bib_target
        return None, None
    if fmt == "markdown":
        if re.search(r"\[@[^\]]+\]", content):
            return "pandoc", _extract_markdown_bibliography(content)
        if re.search(r"^bibliography:\s+(.+)$", content, re.MULTILINE):
            return "pandoc", _extract_markdown_bibliography(content)
        return None, None
    if fmt == "typst":
        bib_match = re.search(r"#bibliography\(([^)]+)\)", content)
        if bib_match or re.search(r"(?<!\w)@[A-Za-z0-9:_-]+", content):
            target = None
            if bib_match:
                path_match = re.search(r'"([^"]+\.bib)"', bib_match.group(1))
                if path_match:
                    target = Path(path_match.group(1))
            return "typst", target
        return None, None
    return None, None


def _extract_markdown_bibliography(content: str) -> Path | None:
    match = re.search(r"^bibliography:\s+(.+)$", content, re.MULTILINE)
    if not match:
        return None
    raw = match.group(1).strip().strip("'\"")
    return Path(raw)


def apply_placements(content: str, placements: list[dict]) -> tuple[str, list[dict]]:
    applied: list[dict] = []
    updated = content
    for placement in placements:
        original = placement["sentence"]
        marked = insert_before_terminal_punctuation(original, placement["citation_marker"])
        if original not in updated:
            placement["writeback_status"] = "skipped"
            placement["writeback_reason"] = "sentence-not-found"
            continue
        updated = updated.replace(original, marked, 1)
        placement["writeback_status"] = "applied"
        applied.append(placement)
    return updated, applied


def update_bibliography(bib_path: Path, placements: list[dict]) -> list[str]:
    existing = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
    appended: list[str] = []
    for placement in placements:
        key = placement["citation_key"]
        if re.search(rf"@\w+\{{{re.escape(key)},", existing):
            continue
        entry = bibtex_entry(placement["candidate"])
        existing = existing.rstrip() + "\n\n" + entry + "\n"
        appended.append(key)
    bib_path.write_text(existing.lstrip("\n"), encoding="utf-8")
    return appended


def main() -> int:
    parser = argparse.ArgumentParser(description="Write verified citation placements back into a paper source.")
    parser.add_argument("paper")
    parser.add_argument("placements_json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--report-json")
    args = parser.parse_args()

    paper_path = Path(args.paper).resolve()
    content = load_text(paper_path)
    fmt = detect_format(paper_path, content).name
    style, bibliography_target = detect_style(fmt, content)
    if style is None:
        raise SystemExit("no recognizable citation style or bibliography target; stay in suggest mode")

    payload = read_json(args.placements_json)
    placements = payload["placements"]
    if fmt == "latex":
        cite_command = style
        for placement in placements:
            placement["citation_marker"] = f"{cite_command}{{{placement['citation_key']}}}"
    elif fmt == "markdown":
        for placement in placements:
            placement["citation_marker"] = f" [@{placement['citation_key']}]"
    elif fmt == "typst":
        for placement in placements:
            placement["citation_marker"] = f" @{placement['citation_key']}"

    updated, applied = apply_placements(content, placements)
    output_path = Path(args.output).resolve()
    output_path.write_text(updated, encoding="utf-8")

    bib_updates: list[str] = []
    if bibliography_target is not None:
        bib_path = (paper_path.parent / bibliography_target).resolve()
        bib_path.parent.mkdir(parents=True, exist_ok=True)
        bib_updates = update_bibliography(bib_path, applied)

    if args.report_json:
        report_path = Path(args.report_json).resolve()
        report = {
            "output_paper": str(output_path),
            "applied": len(applied),
            "skipped": len([p for p in placements if p.get("writeback_status") != "applied"]),
            "bibliography_updates": bib_updates,
            "bibliography_path": str((paper_path.parent / bibliography_target).resolve()) if bibliography_target else None,
        }
        report_path.write_text(__import__("json").dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote paper -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

