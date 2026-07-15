"""
Sidebar: branding, theme switcher, quick KB status, and example questions.

Page navigation itself is handled by st.navigation() in app.py, so this
module only renders the content *around* that native nav widget.
"""

import streamlit as st

from utils import kb_manager


def show_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;margin:2px 0 14px 0;">
                <div style="font-size:26px;">📚</div>
                <div>
                    <div style="font-family:'Fraunces',serif;font-weight:700;font-size:17px;line-height:1.1;">
                        StudyBuddy AI
                    </div>
                    <div style="font-size:11px;color:var(--text-muted);">RAG-powered document Q&A</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Theme switcher
        st.caption("Appearance")
        theme_choice = st.toggle(
            "🌙 Dark mode",
            value=(st.session_state.get("theme", "light") == "dark"),
            key="theme_toggle",
        )
        new_theme = "dark" if theme_choice else "light"
        if new_theme != st.session_state.get("theme", "light"):
            st.session_state.theme = new_theme
            st.rerun()

        st.markdown("---")

        # Knowledge base quick status
        st.caption("Knowledge base")
        try:
            stats = kb_manager.get_kb_stats()
            st.markdown(
                f"""
                <div class="status-pill ok"><span class="dot"></span>Indexed & ready</div>
                <div style="margin-top:8px;font-size:12px;color:var(--text-muted);">
                    📄 {stats['total_documents']} documents · 🧩 {stats['total_chunks']} chunks
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception:
            st.markdown(
                '<div class="status-pill" style="background:var(--surface);color:var(--text-muted);">'
                '<span class="dot"></span>Not yet initialized</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Powered-by badges
        st.caption("Powered by")
        st.markdown(
            """
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:4px;">
                <span class="score-pill">Gemini 2.5 Flash</span>
                <span class="score-pill">ChromaDB</span>
                <span class="score-pill">BGE Embeddings</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Example / suggested questions
        st.caption("💡 Try asking")
        example_questions = [
            "What is Retrieval-Augmented Generation?",
            "Summarize the academic calendar.",
            "What does the AI/ML report conclude?",
        ]
        for q in example_questions:
            if st.button(q, key=f"example_{q}", use_container_width=True):
                st.session_state.pending_question = q
                st.switch_page(st.session_state.get("chat_page_ref", "pages/chat.py"))

        st.markdown("---")
        st.info(
            "Answers are generated only from your uploaded PDFs using "
            "Retrieval-Augmented Generation (RAG).",
            icon="ℹ️",
        )
