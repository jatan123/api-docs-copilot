"""BM25 retrieval over doc chunks, with no external dependencies.

Design choice: start with lexical BM25 instead of embeddings. API questions are full of
exact tokens (endpoint paths, error codes, header names) that keyword search matches
well, it needs no second API key, and it runs offline so the eval suite is free to run.
Embeddings are on the roadmap if evals show paraphrase misses.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from .ingest import Chunk

_STOP = set("""a an and are as at be by can do does for from how i if in is it its me my
of on or so that the this to was we what when where which who why will with you your
should would could get""".split())

# Small domain synonym map: developers' words -> words the docs use.
_SYNONYMS = {
    "hotel": ["property"], "hotels": ["property"], "chain": ["supplier"],
    "perk": ["benefit"], "perks": ["benefit"], "promo": ["offer"], "promotion": ["offer"],
    "deal": ["offer"], "login": ["token", "authentication"], "auth": ["authentication", "token"],
    "authenticate": ["authentication", "token"], "throttle": ["rate", "limit"], "throttled": ["rate", "limit"],
    "expire": ["expires", "expiry", "lifetime"], "expired": ["expired", "expiry"],
    "test": ["sandbox"], "testing": ["sandbox"], "live": ["production"], "prod": ["production"],
    "callback": ["webhook"], "callbacks": ["webhook"], "notify": ["webhook"],
    "breaking": ["version", "major"], "find": ["search"], "lookup": ["search"], "look": ["search"], "deprecated": ["sunset", "version"],
}


def tokenize(text: str) -> list[str]:
    toks = re.findall(r"[a-z0-9_]+", text.lower())
    out = []
    for t in toks:
        if t in _STOP:
            continue
        if len(t) > 4 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        out.append(t)
    return out


def expand(tokens: list[str]) -> list[str]:
    extra = [s for t in tokens for s in _SYNONYMS.get(t, [])]
    return tokens + tokenize(" ".join(extra))


@dataclass
class Hit:
    chunk: Chunk
    score: float


class Retriever:
    def __init__(self, chunks: list[Chunk], k1: float = 1.4, b: float = 0.75, heading_boost: float = 1.0):
        self.chunks = chunks
        self.k1, self.b, self.heading_boost = k1, b, heading_boost
        self.docs = [tokenize(c.text) for c in chunks]
        self.heads = [set(tokenize(f"{c.doc_title} {c.section}")) for c in chunks]
        self.avgdl = sum(map(len, self.docs)) / len(self.docs)
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in self.docs]

    def search(self, query: str, k: int = 4) -> list[Hit]:
        q = expand(tokenize(query))
        scores = []
        for i, tf in enumerate(self.tf):
            dl = len(self.docs[i])
            s = 0.0
            for t in set(q):
                if t not in tf:
                    continue
                f = tf[t]
                s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
                if t in self.heads[i]:
                    s += self.heading_boost * self.idf[t]
            scores.append(s)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [Hit(self.chunks[i], scores[i]) for i in ranked if scores[i] > 0]
