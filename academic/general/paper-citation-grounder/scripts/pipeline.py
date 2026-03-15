#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_step(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the paper citation grounding pipeline.")
    parser.add_argument("paper")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--mode", choices=("suggest", "writeback"), default="suggest")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--min-score", type=int, default=3)
    parser.add_argument("--paragraph-cap", type=int, default=2)
    parser.add_argument("--min-sentence-gap", type=int, default=1)
    args = parser.parse_args()

    base = Path(args.output_dir).resolve()
    base.mkdir(parents=True, exist_ok=True)
    claims_json = base / "claims.json"
    verified_json = base / "verified.json"
    placements_json = base / "placements.json"
    report_prefix = base / "report"

    scripts_dir = Path(__file__).resolve().parent
    python = sys.executable

    run_step(python, str(scripts_dir / "extract_claims.py"), args.paper, "-o", str(claims_json), "--min-score", str(args.min_score))
    run_step(python, str(scripts_dir / "verify_metadata.py"), str(claims_json), args.candidates, "-o", str(verified_json))
    run_step(
        python,
        str(scripts_dir / "place_citations.py"),
        args.paper,
        str(claims_json),
        str(verified_json),
        "-o",
        str(placements_json),
        "--paragraph-cap",
        str(args.paragraph_cap),
        "--min-sentence-gap",
        str(args.min_sentence_gap),
    )
    run_step(python, str(scripts_dir / "build_report.py"), str(claims_json), str(verified_json), str(placements_json), "-o", str(report_prefix))

    if args.mode == "writeback":
        output_paper = base / Path(args.paper).name
        writeback_report = base / "writeback.json"
        run_step(
            python,
            str(scripts_dir / "writeback_citations.py"),
            args.paper,
            str(placements_json),
            "--output",
            str(output_paper),
            "--report-json",
            str(writeback_report),
        )
        print(f"writeback complete -> {output_paper}")

    print(f"pipeline complete -> {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
