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

defaults = {
    "theme": "light",
    "messages": [],
    "search_history": [],
    "pinned_prompts": [],
    "pending_question": None,
    "regenerate_question": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------------------------
# Load CSS
# -------------------------------------------------

load_css(st.session_state.theme)

# -------------------------------------------------
# Pages
# -------------------------------------------------

chat_page = st.Page(
    "pages/chat.py",
    title="Chat",
    icon="💬",
    default=True,
)

dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📊",
)

documents_page = st.Page(
    "pages/documents.py",
    title="Documents",
    icon="📂",
)

settings_page = st.Page(
    "pages/settings.py",
    title="Settings",
    icon="⚙️",
)

about_page = st.Page(
    "pages/about.py",
    title="About",
    icon="ℹ️",
)

# Store page reference
st.session_state.chat_page_ref = chat_page

# -------------------------------------------------
# Navigation
# -------------------------------------------------

nav = st.navigation(
    {
        "StudyBuddy": [
            chat_page,
            dashboard_page,
            documents_page,
        ],
        "": [
            settings_page,
            about_page,
        ],
    }
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

show_sidebar()

# -------------------------------------------------
# Run selected page
# -------------------------------------------------

nav.run()