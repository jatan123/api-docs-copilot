# Roadmap

Prioritised by impact on trust and adoption versus effort.

## Now
- **Run the end-to-end answer eval** and publish `evals/results.md`.
- **Deploy the web UI** (Streamlit Community Cloud, free) so anyone can try it from a link.
- **Held-out eval set:** 20 new questions written *after* tuning, to get an honest accuracy number.

## Next
- **Docs-gap report:** a weekly summary of unanswered and thumbs-down questions for the platform team.
- **Ingest from an OpenAPI spec** as well as Markdown, since most real APIs publish one.
- **Streaming answers** to cut perceived latency.
- **Hybrid retrieval (BM25 + embeddings)**, only if the held-out set shows paraphrase misses.

## Later
- **"Try it" mode:** generate a ready-to-run `curl` for the endpoint the answer cites, against the sandbox.
- **Slack integration:** answer in the channel where partners already ask questions.
- **Multi-API support:** one copilot, several API doc sets, with routing.

## Explicitly not planned
- Executing write calls on a user's behalf. The risk is too high for the value at this stage.
