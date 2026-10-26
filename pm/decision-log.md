# Decision log

Each entry: what I decided, the options, and the evidence.

## 1. Start with keyword retrieval (BM25), not embeddings
**Options:** embeddings + vector DB, or BM25 keyword search.
**Decision:** BM25, implemented in about 60 lines with no dependencies.
**Why:** API questions are full of exact tokens like `/oauth/token`, `429` and `pageSize`, which keyword search matches precisely. It also needs no second API key and runs offline, so the eval suite is free and instant. I'll revisit if evals show misses on paraphrased questions.

## 2. Chunk by doc section, not fixed token windows
**Why:** API docs are already organised by topic. A section is the unit a developer wants, and it gives readable citations ("Authentication › Token lifetime") instead of "chunk 37".

## 3. Tune retrieval against an eval set, not by eyeballing
I wrote 33 questions in a developer's words (28 in-scope, 5 out-of-scope) before tuning anything.

| Change | hit@1 | hit@4 |
|---|---|---|
| Plain BM25 | 54% | 86% |
| + boost matches in section headings | 61% | 96% |
| + small domain synonym map (find → search, perk → benefit, …) | 64% | 100% |

**Caveat:** the same set was used for tuning, so it overstates real-world quality. Next step: a held-out set (see roadmap).

## 4. Drop the "confidence threshold" idea
**Hypothesis:** if the best retrieval score is low, refuse without calling the model. That's cheaper and avoids made-up answers.
**What happened:** at a threshold of 6.0, it wrongly refused 3 real questions and still let 3 of 5 off-topic ones through. Lexical scores don't separate on-topic from off-topic: "How much does Staylane charge per API call?" scores *higher* than many real questions because it shares words with the overview.
**Decision:** keep only a low floor (2.0) for obvious misses, and make the model responsible for refusing, via the grounded prompt with a standard refusal line. Out-of-scope cases are in the answer eval to hold it to that.
**Lesson:** a heuristic that looks right on paper can fail on real data. Measure before you ship it.

## 5. Mandatory citations
**Why:** in a dev workflow, trust comes from verifiability. A cited answer can be checked in seconds, and an uncited one has to be taken on faith. The eval fails any in-scope answer without a valid citation.

## 6. Log everything, including what we couldn't answer
**Why:** for a platform team, the questions the bot *can't* answer are the most valuable output. They're a prioritised list of documentation gaps. Thumbs-down answers become new eval cases.

## 7. Fictional docs for the public demo
**Why:** the idea came from internal API platform work, but internal docs can't be published. A realistic fictional API keeps the demo honest and shareable.
