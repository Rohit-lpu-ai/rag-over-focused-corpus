"""About: project info and footer."""

import streamlit as st

from utils.constants import APP_NAME, APP_VERSION, GITHUB_URL, LICENSE

st.markdown(
    f"""
    <div class="page-hero">
        <div class="eyebrow">About</div>
        <div class="brand-title">ℹ️ About {APP_NAME}</div>
        <div class="brand-subtitle">A RAG-powered study assistant for your own documents.</div>
        <div class="pill-row">
            <span class="score-pill">Traceable answers</span>
            <span class="score-pill">Private knowledge base</span>
            <span class="score-pill">Built with Streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="glass-panel">
    <p>
    StudyBuddy AI lets you upload PDFs -- lecture notes, reports, academic
    calendars -- and ask questions in plain language. Answers are generated
    only from the content you've indexed, with every claim traceable back to
    the exact source chunk it came from.
    </p>
    <p>
    Under the hood: PDFs are split into overlapping chunks, embedded with a
    sentence-transformer model, stored in a persistent ChromaDB collection,
    and retrieved by similarity search before being handed to Gemini for
    answer generation.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.markdown(
    f"""
    <div class="app-footer">
        {APP_NAME} · v{APP_VERSION} ·
        <a href="{GITHUB_URL}" target="_blank">GitHub</a> ·
        {LICENSE} License · Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
