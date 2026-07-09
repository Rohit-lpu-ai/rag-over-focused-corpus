import os
import google.generativeai as genai


def configure_gemini():
    """
    Configure Gemini using the GOOGLE_API_KEY environment variable.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable not found."
        )

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("gemini-2.5-flash")


def build_prompt(query, retrieved_docs):
    """
    Build the prompt using retrieved context.
    """

    context = ""

    for i, doc in enumerate(retrieved_docs, start=1):
        context += (
            f"[Document {i}]\n"
            f"Source: {doc['metadata'].get('source', 'Unknown')}\n"
            f"Chunk: {doc['metadata'].get('chunk_id', 'Unknown')}\n"
            f"Content:\n{doc['text']}\n\n"
        )

    prompt = f"""
You are an AI assistant for StudyBuddy EdTech.

Use ONLY the provided context to answer the user's question.

If the answer is not present in the context, reply exactly:

"I don't know based on the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt


def generate_answer(query, retrieved_docs):
    """
    Generate an answer using Gemini.
    """

    model = configure_gemini()

    prompt = build_prompt(query, retrieved_docs)

    response = model.generate_content(prompt)

    return response.text