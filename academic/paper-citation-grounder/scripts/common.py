#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SOURCE_SCORES = {
    "arxiv": 5,
    "crossref": 5,
    "openalex": 4,
    "semantic-scholar": 4,
    "google-scholar": 2,
}

CLAIM_KEYWORDS = (
    "show",
    "shows",
    "demonstrate",
    "demonstrates",
    "suggest",
    "suggests",
    "outperform",
    "improve",
    "improves",
    "state-of-the-art",
    "sota",
    "novel",
    "first",
    "recent",
    "previous",
    "prior work",
    "literature",
    "studies",
    "evidence",
    "significant",
    "significantly",
    "benchmark",
)


@dataclass
class PaperFormat:
    name: str
    extension: str


def load_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: str | Path, payload: object) -> None:
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: str | Path) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def detect_format(path: str | Path, content: str | None = None) -> PaperFormat:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".tex":
        return PaperFormat("latex", suffix)
    if suffix in {".md", ".markdown"}:
        return PaperFormat("markdown", suffix)
    if suffix in {".typ", ".typst"}:
        return PaperFormat("typst", suffix)
    if suffix == ".pdf":
        return PaperFormat("pdf", suffix)
    if content and "\\begin{" in content:
        return PaperFormat("latex", suffix)
    return PaperFormat("text", suffix)


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def citation_pattern(fmt: str) -> re.Pattern[str]:
    if fmt == "latex":
        return re.compile(r"\\cite\w*\{[^}]+\}")
    if fmt == "markdown":
        return re.compile(r"\[@[^\]]+\]")
    if fmt == "typst":
        return re.compile(r"(?<!\w)@[A-Za-z0-9:_-]+")
    return re.compile(r"$^")


def has_citation_marker(text: str, fmt: str) -> bool:
    return bool(citation_pattern(fmt).search(text))


def split_paragraphs(content: str) -> list[str]:
    paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", content):
        lines = []
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^\\+(documentclass|begin\{document\}|end\{document\}|bibliography|addbibresource)", stripped):
                continue
            if re.match(r"^\\+(section|subsection|subsubsection|chapter)", stripped):
                continue
            if re.match(r"^#(show|set|bibliography)\b", stripped):
                continue
            lines.append(line)
        paragraph = "\n".join(lines).strip()
        if paragraph:
            paragraphs.append(paragraph)
    return paragraphs


def split_sentences(paragraph: str) -> list[str]:
    cleaned = paragraph.replace("\n", " ").strip()
    if not cleaned:
        return []
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\\#])", cleaned)
    return [s.strip() for s in sentences if s.strip()]


def is_heading_like(sentence: str) -> bool:
    stripped = sentence.strip()
    return (
        stripped.startswith("#")
        or stripped.startswith("\\section")
        or stripped.startswith("\\subsection")
        or stripped.startswith("=")
        or stripped.endswith(":")
    )


def claim_score(sentence: str, fmt: str) -> tuple[int, list[str]]:
    reasons: list[str] = []
    stripped = sentence.strip()
    if not stripped or len(stripped) < 30 or is_heading_like(stripped) or stripped.endswith("?"):
        return 0, reasons
    if has_citation_marker(stripped, fmt):
        return 0, ["already-cited"]
    score = 0
    lower = stripped.casefold()
    if any(keyword in lower for keyword in CLAIM_KEYWORDS):
        score += 2
        reasons.append("claim-keyword")
    if re.search(r"\b\d+(\.\d+)?%?\b", stripped):
        score += 2
        reasons.append("numeric-evidence")
    if re.search(r"\b(we|this paper|our method|results|experiments)\b", lower):
        score += 1
        reasons.append("study-language")
    if re.search(r"\b(better|worse|higher|lower|more|less|than)\b", lower):
        score += 1
        reasons.append("comparison")
    if len(stripped) >= 80:
        score += 1
        reasons.append("substantive-length")
    return score, reasons


def generate_citation_key(title: str, authors: Iterable[str], year: object) -> str:
    first_author = next(iter(authors), "ref")
    author_token = normalize_text(first_author).split(" ")[-1] or "ref"
    title_tokens = [token for token in normalize_text(title).split(" ") if token][:2]
    year_token = str(year) if year is not None else "nd"
    key = author_token + year_token + "".join(title_tokens)
    return re.sub(r"[^A-Za-z0-9]+", "", key)[:40] or "ref"


def bibtex_entry(candidate: dict) -> str:
    key = candidate["citation_key"]
    title = candidate["title"]
    authors = " and ".join(candidate.get("authors", []))
    year = candidate.get("year", "")
    venue = candidate.get("venue", "")
    doi = candidate.get("doi")
    url = candidate.get("url")
    lines = [
        f"@article{{{key},",
        f"  title = {{{title}}},",
        f"  author = {{{authors}}},",
        f"  year = {{{year}}},",
    ]
    if venue:
        lines.append(f"  journal = {{{venue}}},")
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    if url:
        lines.append(f"  url = {{{url}}},")
    lines.append("}")
    return "\n".join(lines)


def insert_before_terminal_punctuation(sentence: str, marker: str) -> str:
    match = re.search(r"([.!?])([\"')\]]*)$", sentence)
    if not match:
        return sentence + marker
    punctuation = match.group(1)
    trailing = match.group(2)
    start = match.start(1)
    return sentence[:start] + marker + punctuation + trailing


def render_marker(fmt: str, key: str, cite_command: str = "\\cite") -> str:
    if fmt == "latex":
        return f"{cite_command}{{{key}}}"
    if fmt == "markdown":
        return f" [@{key}]"
    if fmt == "typst":
        return f" @{key}"
    return f" [{key}]"


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")
    return slug or "paper"
