"""Settings: appearance, model info, and session housekeeping."""

import streamlit as st

from utils.constants import EMBEDDING_MODEL, GENERATION_MODEL, VECTOR_DB

st.markdown('<p class="brand-title">⚙️ Settings</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">Preferences for this session</p>', unsafe_allow_html=True)

st.markdown("#### Appearance")
theme_choice = st.radio(
    "Theme",
    ["light", "dark"],
    index=0 if st.session_state.get("theme", "light") == "light" else 1,
    horizontal=True,
    format_func=lambda t: "☀️ Light" if t == "light" else "🌙 Dark",
)
if theme_choice != st.session_state.get("theme", "light"):
    st.session_state.theme = theme_choice
    st.rerun()

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
