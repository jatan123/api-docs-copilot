# 📘 API Docs Copilot

**Ask an API's documentation a question in plain English, and get a grounded answer with citations to the exact section it came from.**

Built by Jatan Parikh, a product manager who owns API platforms, to solve a problem I see constantly: developers integrating with an API waste time hunting through docs or pinging the platform team with questions the docs already answer.

> The demo runs on the docs of **Staylane**, a fictional hotel-partnership API I wrote for this project. It contains no real company's data.

---

## The problem

On an internal API platform, a large share of integration questions are already answered somewhere in the docs. Developers still ask the platform team because:

- docs are long and split across many pages,
- search finds keywords, not answers ("how long does a token last?" ≠ "Token lifetime"),
- a wrong guess is costly: a failed certification or a broken production integration.

Every one of those questions costs a platform PM or engineer time, and slows the partner down.

## Who it's for

| User | Job to be done |
|---|---|
| **Partner developer** integrating the API | "Tell me exactly which endpoint, parameter or limit applies, and show me where it says so." |
| **Platform team** (PM, engineers, support) | "Deflect repeat questions, and show me which questions the docs *don't* answer." |

## What it does

- **Answers from the docs only**, and cites every claim, e.g. `[1]` → *Authentication › Token lifetime*.
- **Says "I couldn't find this in the documentation"** instead of guessing when the docs don't cover something.
- **Handles multi-step questions**, e.g. "I only know the hotel name; how do I get its perks?" → search properties first, then call benefits.
- **Captures feedback**: every question, its sources, latency, token use and a 👍/👎 rating go to a log. Unanswered questions become a to-do list of documentation gaps.

## How it works

```
question ─▶ retrieve top 4 doc sections (BM25 + heading boost + domain synonyms)
         ─▶ floor check: no match at all? → "not in the docs" (no model call)
         ─▶ Claude answers using ONLY those sections, citing [1]..[4]
         ─▶ answer + sources shown in UI ─▶ 👍/👎 logged
```

Key product decisions and the evidence behind them are in [`pm/decision-log.md`](pm/decision-log.md).

## Results

Retrieval is measured offline on a 33-question eval set (28 in-scope, 5 out-of-scope) written as a developer would phrase them, not copied from headings:

| Metric | Baseline (plain BM25) | Current |
|---|---|---|
| Right section in top 4 sent to the model (hit@4) | 86% | **100%** |
| Right section ranked first (hit@1) | 54% | **64%** |

End-to-end answer quality (fact accuracy, citation, and correct refusals) is measured by `evals/run_answer_eval.py`, which writes [`evals/results.md`](evals/results.md).

*Caveat:* the eval set is small and was also used for tuning, so these numbers are optimistic. A held-out set is the next item on the [roadmap](pm/roadmap.md).

## Run it

```bash
git clone https://github.com/jatan123/api-docs-copilot.git
cd api-docs-copilot
pip install -r requirements.txt
cp .env.example .env            # then put your Anthropic API key in .env
export $(cat .env | xargs)

streamlit run app/streamlit_app.py      # web UI
PYTHONPATH=src python -m copilot.cli    # terminal chat
python evals/run_retrieval_eval.py      # offline retrieval eval (no key needed)
python evals/run_answer_eval.py         # end-to-end eval (uses the API)
python -m pytest -q                     # tests (no key needed)
```

To point it at **your own API docs**, replace the Markdown files in `docs/` (one file per topic, `##` headings per section) and update `evals/questions.jsonl`.

## Repo map

```
docs/      fictional Staylane API docs (the knowledge base)
src/       copilot package: ingest → retrieve → answer, plus feedback logging
app/       Streamlit web UI
evals/     eval questions, retrieval eval, end-to-end answer eval
pm/        product brief, decision log, roadmap
tests/     offline tests (fake model client, no API key needed)
```

## Product docs

- [Product brief](pm/product-brief.md): problem, users, success metrics, non-goals
- [Decision log](pm/decision-log.md): what I chose, what I tried that didn't work, and why
- [Roadmap](pm/roadmap.md): what's next and how I'd prioritise it

---

Built with Python, Streamlit and the Claude API. MIT licensed.
