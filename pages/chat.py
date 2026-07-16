"""Chat page: ask questions, see cited answers, manage prompt history."""

from datetime import datetime

import streamlit as st

from pyfiles.retrieval import retrieve_documents
from pyfiles.generation import generate_answer
from utils import stats_tracker
from utils.constants import APP_NAME, APP_TAGLINE

USER_AVATAR = "🧑‍🎓"
AI_AVATAR = "📚"


def _run_pipeline(question: str):
    """Run retrieval + generation, showing a step-by-step status trail."""
    with st.status("Thinking...", expanded=True) as status:
        st.write("🔍 Searching documents...")
        docs = retrieve_documents(question)

        st.write("🧩 Reading retrieved context...")
        start = datetime.now()

        st.write("✍️ Generating answer...")
        answer = generate_answer(question, docs)

        elapsed = (datetime.now() - start).total_seconds()
        status.update(label="Answer ready", state="complete", expanded=False)

    stats_tracker.record_query(elapsed)
    return docs, answer


def _render_sources(docs: list) -> None:
    if not docs:
        return
    st.markdown("**📄 Retrieved sources**")
    for i, doc in enumerate(docs, start=1):
        meta = doc.get("metadata", {})
        source = meta.get("source", "Unknown")
        chunk_id = meta.get("chunk_id", "Unknown")
        distance = doc.get("distance")
        score_str = f"{distance:.4f}" if isinstance(distance, (int, float)) else "n/a"
        preview = (doc.get("text") or "")[:220].strip()
        if len(doc.get("text") or "") > 220:
            preview += "..."

        st.markdown(
            f"""
            <div class="source-card">
                <span class="source-badge">{i}</span>
                <span class="source-name">{source}</span>
                <div class="source-meta">chunk #{chunk_id} · distance {score_str}</div>
                <div class="source-preview">{preview}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("View full chunk", expanded=False):
            st.write(doc.get("text", ""))


def _render_message(msg: dict, index: int) -> None:
    avatar = USER_AVATAR if msg["role"] == "user" else AI_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            _render_sources(msg.get("sources", []))

            ts = msg.get("timestamp", "")
            st.markdown(f'<div class="msg-meta">🕒 {ts}</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("📋 Copy", key=f"copy_{index}"):
                    st.toast("Answer copied to view -- select text above to copy.", icon="📋")
            with col2:
                st.download_button(
                    "⬇️ Save",
                    data=msg["content"],
                    file_name=f"studybuddy_answer_{index}.md",
                    mime="text/markdown",
                    key=f"dl_{index}",
                )
            if index == len(st.session_state.messages) - 1:
                with col3:
                    if st.button("🔄 Regenerate", key=f"regen_{index}"):
                        st.session_state.regenerate_question = msg.get("question")
                        st.rerun()


# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(f'<p class="brand-title">📚 {APP_NAME}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="brand-subtitle">{APP_TAGLINE}</p>', unsafe_allow_html=True)

with st.expander("💡 Suggested prompts & recent questions", expanded=False):
    tab1, tab2 = st.tabs(["Suggested", "Recent"])
    with tab1:
        for q in [
            "What is Retrieval-Augmented Generation?",
            "Explain Dynamic CRM Personalization.",
            "Summarize the Academic Calendar.",
        ]:
            c1, c2 = st.columns([5, 1])
            c1.write(f"• {q}")
            if c2.button("Ask", key=f"suggest_{q}"):
                st.session_state.pending_question = q
                st.rerun()
    with tab2:
        if not st.session_state.search_history:
            st.caption("No recent questions yet.")
        else:
            for q in reversed(st.session_state.search_history[-8:]):
                c1, c2 = st.columns([5, 1])
                c1.write(f"• {q}")
                if c2.button("Ask", key=f"recent_{q}_{id(q)}"):
                    st.session_state.pending_question = q
                    st.rerun()
            if st.button("🗑️ Clear recent history"):
                st.session_state.search_history = []
                st.rerun()

st.divider()

# -------------------------------------------------
# Message history
# -------------------------------------------------
for i, message in enumerate(st.session_state.messages):
    _render_message(message, i)

# -------------------------------------------------
# Handle pending / regenerate / new input
# -------------------------------------------------
incoming_question = None
if "pending_question" in st.session_state:
    incoming_question = st.session_state.pop("pending_question")
if "regenerate_question" in st.session_state:
    incoming_question = st.session_state.pop("regenerate_question")

typed_question = st.chat_input("Ask a question about your documents...")
question = incoming_question or typed_question

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question, "timestamp": datetime.now().strftime("%H:%M:%S")}
    )
    st.session_state.search_history.append(question)

    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(question)

    with st.chat_message("assistant", avatar=AI_AVATAR):
        try:
            docs, answer = _run_pipeline(question)
        except Exception as e:
            st.error(f"Something went wrong while answering: {e}")
            st.stop()

        st.markdown(answer)
        _render_sources(docs)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": docs,
            "question": question,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
    )
    st.rerun()
