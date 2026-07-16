"""Chat page: ask questions, see cited answers, manage prompt history."""

import json
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from pyfiles.retrieval import retrieve_documents
from pyfiles.generation import generate_answer
from utils import stats_tracker
from utils.constants import APP_NAME, APP_TAGLINE

USER_AVATAR = "🧑‍🎓"
AI_AVATAR = "📚"


def _render_voice_assistant() -> None:
    """Render a lightweight browser voice UI for speech-to-text."""
    components.html(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--border);border-radius:14px;background:var(--bg-elevated);box-shadow:var(--shadow);max-width:460px;margin:10px 0 12px 0;">
            <button id="voice-btn" style="border:none;border-radius:999px;padding:10px 14px;background:var(--primary);color:var(--primary-text);font-weight:600;cursor:pointer;">🎤 Start listening</button>
            <div id="voice-status" style="font-size:13px;color:var(--text-muted);">Tap to speak a question.</div>
        </div>
        <script>
            const btn = document.getElementById('voice-btn');
            const status = document.getElementById('voice-status');
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition = null;

            if (SpeechRecognition) {
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';
                recognition.onstart = () => {
                    btn.textContent = '🛑 Stop';
                    status.textContent = 'Listening...';
                    btn.dataset.listening = 'true';
                };
                recognition.onresult = (event) => {
                    const transcript = Array.from(event.results).map((r) => r[0].transcript).join(' ').trim();
                    if (transcript) {
                        status.textContent = 'Heard: ' + transcript;
                        const url = new URL(window.location.href);
                        url.searchParams.set('voice_question', transcript);
                        window.history.replaceState({}, '', url);
                        window.location.reload();
                    } else {
                        status.textContent = 'No speech detected.';
                    }
                };
                recognition.onerror = () => {
                    status.textContent = 'Voice input is unavailable in this browser.';
                    btn.textContent = '🎤 Start listening';
                    btn.dataset.listening = 'false';
                };
                recognition.onend = () => {
                    btn.textContent = '🎤 Start listening';
                    btn.dataset.listening = 'false';
                };
            } else {
                status.textContent = 'Voice input is not supported in this browser.';
                btn.disabled = true;
            }

            btn.onclick = () => {
                if (!recognition) return;
                if (btn.dataset.listening === 'true') {
                    recognition.stop();
                    return;
                }
                recognition.start();
            };
        </script>
        """,
        height=120,
    )


def _render_voice_output(text: str) -> None:
    """Render a tiny hidden component that speaks the provided text."""
    if not text:
        return
    components.html(
        f"""
        <script>
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance({json.dumps(text)});
                utterance.lang = 'en-US';
                utterance.rate = 1.0;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }}
        </script>
        """,
        height=0,
    )


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
st.markdown(
    f"""
    <div class="page-hero">
        <div class="eyebrow">Study workspace</div>
        <div class="brand-title">📚 {APP_NAME}</div>
        <div class="brand-subtitle">{APP_TAGLINE}</div>
        <div class="pill-row">
            <span class="score-pill">Grounded answers</span>
            <span class="score-pill">Traceable sources</span>
            <span class="score-pill">Private documents</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

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

st.markdown(
    """
    <div class="mini-card">
        <div class="mini-title">How this workspace works</div>
        <div class="mini-sub">
            Ask a question, review the grounded answer, and inspect the source chunks that support it.
            Everything stays anchored to the documents you uploaded.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

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

voice_question = st.query_params.get("voice_question", [""])[0].strip()
if voice_question:
    incoming_question = voice_question
    st.query_params.clear()

st.markdown("<div style='margin: 0 0 8px 0;'>", unsafe_allow_html=True)
_render_voice_assistant()
st.markdown("</div>", unsafe_allow_html=True)

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
            if not answer or not str(answer).strip():
                raise ValueError("The model returned an empty response.")
        except Exception as e:
            st.error(f"Something went wrong while answering: {e}")
            st.stop()

        st.markdown(answer)
        _render_voice_output(answer)
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
