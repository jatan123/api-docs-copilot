"""End-to-end answer eval — calls Claude, needs ANTHROPIC_API_KEY.

Scores each answer with simple deterministic checks:
- in-scope:  contains every required fact (must_include) AND cites at least one valid source
- out-of-scope: declines with the standard "couldn't find this" message
Writes evals/results.md so the numbers can be quoted in the README.

    python evals/run_answer_eval.py
"""

import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from copilot.answer import NOT_FOUND, Copilot  # noqa: E402


def grade(q: dict, a) -> tuple[bool, str]:
    if not q["expected"]:
        ok = a.text.startswith(NOT_FOUND)
        return ok, "declined" if ok else "answered an out-of-scope question"
    text = a.text.lower()
    missing = [m for m in q["must_include"] if m.lower() not in text]
    valid_cites = {n for n in a.cited_numbers if 1 <= n <= len(a.sources)}
    if missing:
        return False, f"missing {missing}"
    if not valid_cites:
        return False, "no valid citation"
    return True, "ok"


def main() -> None:
    bot = Copilot(docs_dir=str(ROOT / "docs"))
    qs = [json.loads(l) for l in (ROOT / "evals/questions.jsonl").read_text().splitlines() if l.strip()]
    rows = []
    for q in qs:
        a = bot.ask(q["question"])
        ok, why = grade(q, a)
        rows.append({**q, "ok": ok, "why": why, "latency_ms": a.latency_ms,
                     "tokens": a.input_tokens + a.output_tokens, "answer": a.text})
        print(f"{'PASS' if ok else 'FAIL'} {q['id']} {why}")
        time.sleep(0.5)

    def rate(cat):
        sel = [r for r in rows if r["category"] == cat]
        return f"{sum(r['ok'] for r in sel)}/{len(sel)}"

    ins = [r for r in rows if r["expected"]]
    oos = [r for r in rows if not r["expected"]]
    lat = [r["latency_ms"] for r in rows if r["tokens"]]
    summary = {
        "model": bot.model,
        "overall_pass": f"{sum(r['ok'] for r in rows)}/{len(rows)}",
        "in_scope_accuracy": f"{sum(r['ok'] for r in ins)}/{len(ins)}",
        "lookup": rate("lookup"), "multi_hop": rate("multi_hop"),
        "out_of_scope_declined": f"{sum(r['ok'] for r in oos)}/{len(oos)}",
        "median_latency_ms": int(statistics.median(lat)) if lat else None,
        "avg_tokens_per_answer": int(statistics.mean(r["tokens"] for r in rows if r["tokens"])) if lat else None,
    }

    out = ["# Answer eval results", "", f"Run: {time.strftime('%Y-%m-%d %H:%M')}", ""]
    out += [f"- **{k.replace('_', ' ')}**: {v}" for k, v in summary.items()]
    out += ["", "## Failures", ""]
    out += [f"- `{r['id']}` {r['question']} — {r['why']}" for r in rows if not r["ok"]] or ["None"]
    (ROOT / "evals/results.md").write_text("\n".join(out) + "\n")
    print(json.dumps(summary, indent=2))
    print("Wrote evals/results.md")


if __name__ == "__main__":
    main()
