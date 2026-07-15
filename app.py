"""
StudyBuddy AI -- entry point.

This file owns page config, theme/session bootstrap, and native Streamlit
navigation (st.navigation). Each page under pages/ is a self-contained view;
none of them touch pyfiles/ backend logic directly except through
utils/kb_manager.py, which is additive and documented separately.
"""

import streamlit as st

from components.styles import load_css
from components.sidebar import show_sidebar

# -------------------------------------------------
# Page config (must be the first Streamlit call)
# -------------------------------------------------
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Session bootstrap
# -------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "pinned_prompts" not in st.session_state:
    st.session_state.pinned_prompts = []

load_css(st.session_state.theme)

# -------------------------------------------------
# Pages
# -------------------------------------------------
chat_page = st.Page("pages/chat.py", title="Chat", icon="💬", default=True)
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
documents_page = st.Page("pages/documents.py", title="Documents", icon="📂")
settings_page = st.Page("pages/settings.py", title="Settings", icon="⚙️")
about_page = st.Page("pages/about.py", title="About", icon="ℹ️")

st.session_state.chat_page_ref = chat_page

nav = st.navigation(
    {
        "StudyBuddy": [chat_page, dashboard_page, documents_page],
        "": [settings_page, about_page],
    }
)

show_sidebar()

nav.run()
