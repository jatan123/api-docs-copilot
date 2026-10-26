"""Offline retrieval eval — no API key needed.

Measures, for in-scope questions, whether the right doc section is retrieved
(hit@1, and hit@4 — the 4 sections actually sent to the model), and for out-of-scope questions, whether the retrieval gate
correctly declines before calling the model.

    python evals/run_retrieval_eval.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from copilot.ingest import load_chunks  # noqa: E402
from copilot.retrieve import Retriever  # noqa: E402

MIN_SCORE = 2.0  # keep in sync with Copilot(min_score=...)


def run(min_score: float = MIN_SCORE, verbose: bool = True) -> dict:
    r = Retriever(load_chunks(ROOT / "docs"))
    qs = [json.loads(l) for l in (ROOT / "evals/questions.jsonl").read_text().splitlines() if l.strip()]
    ins = [q for q in qs if q["expected"]]
    oos = [q for q in qs if not q["expected"]]

    h1 = h4 = gated_wrongly = 0
    misses = []
    for q in ins:
        hits = r.search(q["question"], k=4)
        ids = [h.chunk.id for h in hits]
        if hits and hits[0].score < min_score:
            gated_wrongly += 1
            misses.append((q["id"], "declined (score %.1f)" % hits[0].score))
            continue
        if ids and ids[0] in q["expected"]:
            h1 += 1
        if any(i in q["expected"] for i in ids):
            h4 += 1
        else:
            misses.append((q["id"], f"got {ids[:2]}"))

    declined = 0
    for q in oos:
        hits = r.search(q["question"], k=1)
        if not hits or hits[0].score < min_score:
            declined += 1
        else:
            misses.append((q["id"], f"OOS passed floor; model must refuse. top= {hits[0].chunk.id} ({hits[0].score:.1f})"))

    res = {
        "in_scope_questions": len(ins),
        "hit@1": round(h1 / len(ins), 3),
        "hit@4": round(h4 / len(ins), 3),
        "in_scope_wrongly_declined": gated_wrongly,
        "out_of_scope_questions": len(oos),
        "out_of_scope_declined": round(declined / len(oos), 3),
    }
    if verbose:
        print(json.dumps(res, indent=2))
        for m in misses:
            print("  miss:", *m)
    return res


if __name__ == "__main__":
    run()
