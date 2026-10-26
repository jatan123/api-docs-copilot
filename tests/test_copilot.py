import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "evals"))

from copilot import Copilot, load_chunks  # noqa: E402
from copilot.answer import NOT_FOUND  # noqa: E402
from copilot.ingest import split_markdown  # noqa: E402
from run_answer_eval import grade  # noqa: E402
from run_retrieval_eval import run as run_retrieval  # noqa: E402

DOCS = ROOT / "docs"


class FakeClient:
    """Stands in for the Anthropic client so tests run offline."""

    def __init__(self, reply):
        self.reply, self.calls = reply, []
        self.messages = self

    def create(self, **kw):
        self.calls.append(kw)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self.reply)],
                               usage=SimpleNamespace(input_tokens=500, output_tokens=60))


def test_chunks_split_on_sections():
    chunks = split_markdown("x", "# Title\n\nintro\n\n## A\nalpha\n\n## B\nbeta\n")
    assert [c.section for c in chunks] == ["Introduction", "A", "B"]
    assert chunks[1].id == "x#a" and "alpha" in chunks[1].text


def test_retrieval_finds_token_lifetime():
    bot = Copilot(docs_dir=str(DOCS), client=FakeClient("x"))
    assert bot.retrieve("how long does a token last before it expires")[0].chunk.id == "02-authentication#token-lifetime"


def test_floor_declines_without_calling_model():
    fake = FakeClient("should not be called")
    a = Copilot(docs_dir=str(DOCS), client=fake).ask("zzqx blorp")
    assert a.text.startswith(NOT_FOUND) and not a.answered_from_docs and fake.calls == []


def test_answer_passes_sources_and_system_prompt():
    fake = FakeClient("Tokens last 3600 seconds [1].")
    a = Copilot(docs_dir=str(DOCS), client=fake).ask("How long is an access token good for?")
    call = fake.calls[0]
    assert "Answer ONLY from the numbered sources" in call["system"]
    assert "<source id=\"1\"" in call["messages"][-1]["content"]
    assert a.cited_numbers == {1} and a.input_tokens == 500


def test_grader():
    q = {"expected": ["a"], "must_include": ["3600"]}
    good = SimpleNamespace(text="3600 seconds [1]", cited_numbers={1}, sources=[1])
    uncited = SimpleNamespace(text="3600 seconds", cited_numbers=set(), sources=[1])
    assert grade(q, good)[0] and not grade(q, uncited)[0]
    oos = {"expected": [], "must_include": []}
    assert grade(oos, SimpleNamespace(text=NOT_FOUND + " ..."))[0]


def test_retrieval_quality_does_not_regress():
    res = run_retrieval(verbose=False)
    assert res["hit@4"] >= 0.95 and res["in_scope_wrongly_declined"] == 0


def test_docs_contain_no_employer_material():
    banned = ["american express", "amex", "aexp", "maps api", "centurion"]
    text = " ".join(c.text.lower() for c in load_chunks(DOCS))
    assert not [b for b in banned if b in text]
