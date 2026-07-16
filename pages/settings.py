"""Settings: appearance, model info, and session housekeeping."""

import streamlit as st

from utils.constants import EMBEDDING_MODEL, GENERATION_MODEL, VECTOR_DB

st.markdown(
    """
    <div class="page-hero">
        <div class="eyebrow">Preferences</div>
        <div class="brand-title">⚙️ Settings</div>
        <div class="brand-subtitle">Preferences for this session</div>
        <div class="pill-row">
            <span class="score-pill">Theme controls</span>
            <span class="score-pill">Session tools</span>
            <span class="score-pill">Model reference</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### Appearance")
st.markdown('<div class="theme-picker-card">', unsafe_allow_html=True)
current_theme = st.session_state.get("theme", "light")
col1, col2 = st.columns(2)
with col1:
    if st.button(
        "☀️ Light",
        use_container_width=True,
        type="primary" if current_theme == "light" else "secondary",
        key="settings_theme_light",
    ):
        st.session_state.theme = "light"
        st.rerun()
with col2:
    if st.button(
        "🌙 Dark",
        use_container_width=True,
        type="primary" if current_theme == "dark" else "secondary",
        key="settings_theme_dark",
    ):
        st.session_state.theme = "dark"
        st.rerun()

st.markdown(
    f'<div class="theme-preview"><span class="dot"></span>{"Night study mode" if current_theme == "dark" else "Bright reading mode"}</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown("#### AI configuration")
st.caption("These are fixed by the backend pipeline and shown here for reference.")
c1, c2, c3 = st.columns(3)
c1.markdown(f"**Generation model**\n\n{GENERATION_MODEL}")
c2.markdown(f"**Embedding model**\n\n{EMBEDDING_MODEL}")
c3.markdown(f"**Vector database**\n\n{VECTOR_DB}")

st.divider()

st.markdown("#### Session data")
c1, c2 = st.columns(2)
with c1:
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.toast("Chat history cleared.", icon="🗑️")
        st.rerun()
with c2:
    if st.button("🗑️ Clear recent-question history", use_container_width=True):
        st.session_state.search_history = []
        st.toast("Search history cleared.", icon="🗑️")
        st.rerun()
