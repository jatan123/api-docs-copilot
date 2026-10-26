"""Log every question, answer and thumbs-up/down rating to a local JSONL file.

This is the product feedback loop: unanswered questions show which docs are missing,
and thumbs-down answers become new eval cases.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

LOG_PATH = Path("logs/interactions.jsonl")


def log_interaction(answer, rating: str | None = None, path: Path = LOG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": answer.question,
        "answered_from_docs": answer.answered_from_docs,
        "sources": [c.id for c in answer.sources],
        "latency_ms": answer.latency_ms,
        "input_tokens": answer.input_tokens,
        "output_tokens": answer.output_tokens,
        "model": answer.model,
        "rating": rating,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def summarize(path: Path = LOG_PATH) -> dict:
    if not path.exists():
        return {"questions": 0}
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    rated = [r for r in rows if r["rating"]]
    return {
        "questions": len(rows),
        "unanswered_rate": round(sum(not r["answered_from_docs"] for r in rows) / len(rows), 3),
        "thumbs_up_rate": round(sum(r["rating"] == "up" for r in rated) / len(rated), 3) if rated else None,
        "median_latency_ms": sorted(r["latency_ms"] for r in rows)[len(rows) // 2],
        "top_unanswered": [r["question"] for r in rows if not r["answered_from_docs"]][-10:],
    }
