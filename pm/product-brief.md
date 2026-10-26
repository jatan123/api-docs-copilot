# Product brief: API Docs Copilot

## Problem
Developers integrating with an API ask the platform team questions the documentation already answers. That costs them hours of waiting and costs the platform team engineering and support time. Keyword search doesn't fix it, because developers ask in their own words ("how long does a token last?"), not the docs' words ("Token lifetime").

## Users
1. **Partner developer (primary).** Mid-integration, under deadline, wants a precise answer they can trust and verify.
2. **Platform team (secondary).** Wants fewer repeat questions and visibility into where the docs fall short.

## Goals and success metrics
| Goal | Metric | Target for v1 | How it's measured |
|---|---|---|---|
| Answers are correct | Fact accuracy on in-scope eval questions | ≥ 90% | `evals/run_answer_eval.py` |
| Answers are verifiable | Share of answers with a valid citation | 100% | same |
| No made-up answers | Out-of-scope questions correctly declined | 100% | same |
| Retrieval finds the right section | hit@4 | ≥ 95% | `evals/run_retrieval_eval.py` |
| Users find it helpful | 👍 rate on rated answers | ≥ 80% | `logs/interactions.jsonl` |
| Docs get better | Unanswered questions reviewed weekly | 100% reviewed | log summary |
| Fast enough to use mid-task | Median latency | < 5 s | log |

**North-star metric (in a real deployment):** share of partner integration questions resolved without a human, measured as fewer support tickets per active partner.

## Non-goals (v1)
- Making API calls on the user's behalf.
- Answering questions about anything other than the provided docs.
- Account-specific questions ("why did *my* request fail?"). These need logs and authentication, not docs.

## Risks and mitigations
| Risk | Mitigation |
|---|---|
| Confident wrong answers | Grounded prompt, mandatory citations, standard "not in the docs" refusal, out-of-scope eval cases |
| Docs go stale and the bot repeats stale info | Answers cite sections, so fixing a doc fixes the answer; there is no separate copy to maintain |
| Prompt injection via docs or questions | Sources are wrapped as data and the system prompt says to ignore instructions inside them |
| Leaked credentials | API key only from environment or secrets store; `.env` is gitignored |
| Cost growth | Floor check skips the model on obvious misses; token use is logged per answer |
