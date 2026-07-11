import streamlit as st

from pyfiles.retrieval import retrieve_documents
from pyfiles.generation import generate_answer

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="StudyBuddy RAG",
    page_icon="📚",
    layout="wide",
)

# ----------------------------
# Title
# ----------------------------
st.title("📚 StudyBuddy RAG")
st.markdown(
    "Ask questions about your uploaded documents using Retrieval-Augmented Generation (RAG)."
)

st.divider()

# ----------------------------
# Question Input
# ----------------------------
query = st.text_input(
    "Enter your question:",
    placeholder="Example: What is Retrieval-Augmented Generation?",
)

# ----------------------------
# Ask Button
# ----------------------------
if st.button("Ask"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching documents and generating answer..."):

        retrieved_docs = retrieve_documents(query)

        answer = generate_answer(
            query,
            retrieved_docs,
        )

    st.success("Answer generated successfully!")

    st.subheader("🤖 Answer")

    st.write(answer)

    st.divider()

    st.subheader("📄 Retrieved Sources")

    for i, doc in enumerate(retrieved_docs, start=1):

        with st.expander(
            f"Source {i} | {doc['metadata'].get('source','Unknown')}"
        ):

            st.write(
                f"**Chunk ID:** {doc['metadata'].get('chunk_id','Unknown')}"
            )

            st.write(
                f"**Similarity Distance:** {doc['distance']:.4f}"
            )

            st.write(doc["text"])