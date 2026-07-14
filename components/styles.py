import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .main-title{
        font-size:42px;
        font-weight:700;
        color:#2E86C1;
        margin-bottom:0px;
    }

    .subtitle{
        font-size:18px;
        color:#6c757d;
        margin-top:-10px;
        margin-bottom:20px;
    }

    .metric-card{
        background:#F8F9FA;
        padding:15px;
        border-radius:10px;
        border:1px solid #E5E7EB;
    }

    .answer-box{
        background:#F8F9FA;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #2E86C1;
    }

    .footer{
        text-align:center;
        color:gray;
        font-size:14px;
        margin-top:30px;
    }

    </style>
    """, unsafe_allow_html=True)