"""Web UI: streamlit run app/streamlit_app.py"""

import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from copilot import Copilot  # noqa: E402
from copilot.feedback import log_interaction  # noqa: E402

st.set_page_config(page_title="API Docs Copilot", page_icon="📘", layout="centered")

# Streamlit Cloud stores secrets in st.secrets; locally use an environment variable.
try:
    if "ANTHROPIC_API_KEY" in st.secrets:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass


@st.cache_resource
def get_bot() -> Copilot:
    return Copilot(docs_dir=str(ROOT / "docs"))


bot = get_bot()

with st.sidebar:
    st.header("About")
    st.write("Ask questions about the **Staylane Partner API**, a fictional hotel-partnership API. "
             "Every answer is grounded in the docs and cites the sections it used.")
    st.caption("If the docs don't cover something, the copilot says so instead of guessing.")
    st.divider()
    st.subheader("Try asking")
    examples = [
        "How long does an access token last?",
        "How do I get benefits if I only know the hotel name?",
        "What should I do when I get a 429?",
        "Can I combine two offers on one booking?",
        "What do I need to get production access?",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex

st.title("📘 API Docs Copilot")
st.caption("Grounded answers with citations · built with the Claude API")

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Sources"):
                for n, label in enumerate(m["sources"], 1):
                    st.markdown(f"**[{n}]** {label}")
        if m["role"] == "assistant" and m.get("answer") is not None and not m.get("rated"):
            c1, c2, _ = st.columns([1, 1, 8])
            if c1.button("👍", key=f"up{i}"):
                log_interaction(m["answer"], "up"); m["rated"] = True; st.rerun()
            if c2.button("👎", key=f"down{i}"):
                log_interaction(m["answer"], "down"); m["rated"] = True; st.rerun()

question = st.chat_input("Ask about the API…") or st.session_state.pop("pending", None)
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    try:
        with st.spinner("Searching the docs…"):
            a = bot.ask(question)
        log_interaction(a)
        st.session_state.messages.append({
            "role": "assistant", "content": a.text, "answer": a,
            "sources": [c.label for c in a.sources],
        })
    except RuntimeError as e:
        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {e}"})
    st.rerun()
