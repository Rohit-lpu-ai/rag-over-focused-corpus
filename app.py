import streamlit as st

from pyfiles.retrieval import retrieve_documents
from pyfiles.generation import generate_answer

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="📚",
    layout="wide",
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown("""
<style>

.main-title{
    font-size:42px;
    font-weight:bold;
    color:#2E86C1;
}

.subtitle{
    font-size:18px;
    color:gray;
    margin-bottom:20px;
}

.answer-box{
    background:#F4F6F7;
    padding:18px;
    border-radius:10px;
    border-left:6px solid #2E86C1;
}

.source-box{
    background:#FBFCFC;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:

    st.title("📚 StudyBuddy AI")

    st.markdown("---")

    st.subheader("⚙ Powered By")

    st.success("Gemini 2.5 Flash")

    st.success("ChromaDB")

    st.success("Sentence Transformers")

    st.success("Streamlit")

    st.markdown("---")

    st.subheader("💡 Example Questions")

    st.write("• What is Retrieval-Augmented Generation?")

    st.write("• Explain Dynamic CRM Personalization.")

    st.write("• Summarize the Academic Calendar.")

    st.markdown("---")

    st.info(
        "This application answers questions from uploaded PDFs using Retrieval-Augmented Generation (RAG)."
    )

# -------------------------------------------------
# Header
# -------------------------------------------------

st.markdown(
    '<p class="main-title">📚 StudyBuddy AI</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="subtitle">AI-Powered Document Question Answering using RAG + Gemini</p>',
    unsafe_allow_html=True,
)

st.divider()

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# Chat Input
# -------------------------------------------------

question = st.chat_input("Ask a question about your documents...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Searching documents..."):

        try:

            docs = retrieve_documents(question)

            answer = generate_answer(question, docs)

        except Exception as e:

            st.error(str(e))

            st.stop()

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    with st.chat_message("assistant"):

        st.markdown(answer)

        st.divider()

        st.subheader("📄 Retrieved Sources")

        for i, doc in enumerate(docs, start=1):

            with st.expander(
                f"📄 {doc['metadata'].get('source','Unknown')}"
            ):

                st.markdown(
                    f"**Chunk ID:** {doc['metadata'].get('chunk_id','Unknown')}"
                )

                st.markdown(
                    f"**Similarity Distance:** `{doc['distance']:.4f}`"
                )

                st.markdown("---")

                st.write(doc["text"])