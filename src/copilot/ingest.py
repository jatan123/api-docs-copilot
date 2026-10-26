"""Load Markdown docs and split them into section-level chunks.

Design choice: chunk on `##` headings rather than fixed token windows. API docs are
already organised by topic, so a section ("Token lifetime", "Rate limits") is the unit
a developer actually wants, and it makes citations readable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    id: str          # e.g. "02-authentication#token-lifetime"
    doc_title: str   # e.g. "Authentication"
    section: str     # e.g. "Token lifetime"
    text: str        # section body, including the doc title for context

    @property
    def label(self) -> str:
        return f"{self.doc_title} › {self.section}"


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def split_markdown(name: str, md: str) -> list[Chunk]:
    lines = md.splitlines()
    doc_title = name
    if lines and lines[0].startswith("# "):
        doc_title = lines[0][2:].strip()
        lines = lines[1:]

    sections: list[tuple[str, list[str]]] = [("Introduction", [])]
    for line in lines:
        if line.startswith("## "):
            sections.append((line[3:].strip(), []))
        else:
            sections[-1][1].append(line)

    chunks = []
    for section, body in sections:
        text = "\n".join(body).strip()
        if not text:
            continue
        chunks.append(Chunk(
            id=f"{name}#{_slug(section)}",
            doc_title=doc_title,
            section=section,
            text=f"{doc_title} — {section}\n\n{text}",
        ))
    return chunks


def load_chunks(docs_dir: str | Path) -> list[Chunk]:
    docs_dir = Path(docs_dir)
    chunks: list[Chunk] = []
    for path in sorted(docs_dir.glob("*.md")):
        chunks.extend(split_markdown(path.stem, path.read_text(encoding="utf-8")))
    if not chunks:
        raise ValueError(f"No Markdown docs found in {docs_dir}")
    return chunks
