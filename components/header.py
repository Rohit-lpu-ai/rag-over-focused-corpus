import streamlit as st

def show_header():
    st.markdown(
        '<p class="main-title">📚 StudyBuddy AI</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="subtitle">AI-Powered Document Question Answering using RAG + Gemini</p>',
        unsafe_allow_html=True,
    )

    st.divider()

    