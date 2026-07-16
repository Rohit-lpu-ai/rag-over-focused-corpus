import streamlit as st

def initialize_session():

    defaults = {
        "messages": [],
        "search_history": [],
        "pending_question": None,
        "regenerate_question": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value