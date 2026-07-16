# import importlib.util
# import os
# from pathlib import Path

# from dotenv import load_dotenv

# try:
#     import google.generativeai as genai
# except ImportError:  # pragma: no cover - defensive fallback for environments without SDK
#     genai = None

# GENAI_AVAILABLE = importlib.util.find_spec("google.generativeai") is not None

# load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


# def configure_gemini():
#     """
#     Configure Gemini using the GOOGLE_API_KEY environment variable.
#     """

#     if genai is None or not GENAI_AVAILABLE:
#         raise ImportError(
#             "The 'google-generativeai' package could not be imported in the current Python environment. "
#             "Please run the app from the project virtual environment or install the package with 'pip install google-generativeai'."
#         )

#     api_key = os.getenv("GOOGLE_API_KEY")

#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY environment variable not found.")

#     genai.configure(api_key=api_key)

#     return genai.GenerativeModel("gemini-2.5-flash")


# def build_prompt(query, retrieved_docs):
#     """
#     Build the prompt using retrieved context.
#     """

#     context = ""

#     for i, doc in enumerate(retrieved_docs, start=1):
#         context += (
#             f"[Document {i}]\n"
#             f"Source: {doc['metadata'].get('source', 'Unknown')}\n"
#             f"Chunk: {doc['metadata'].get('chunk_id', 'Unknown')}\n"
#             f"Content:\n{doc['text']}\n\n"
#         )

#     prompt = f"""
# You are an AI assistant for StudyBuddy EdTech.

# Use ONLY the provided context to answer the user's question.

# If the answer is not present in the context, reply exactly:

# "I don't know based on the provided documents."

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     return prompt


# def generate_answer(query, retrieved_docs):
#     """
#     Generate an answer using Gemini.
#     """

#     model = configure_gemini()

#     prompt = build_prompt(query, retrieved_docs)

#     response = model.generate_content(prompt)

#     return response.text

import os
from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------------
# Import Gemini SDK
# --------------------------------------------------

try:
    import google.generativeai as genai

    GENAI_AVAILABLE = True
    print("✅ Google Generative AI imported successfully.")

except Exception as e:
    GENAI_AVAILABLE = False
    genai = None

    print("❌ Failed to import google.generativeai")
    print("Reason:", e)

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv(
    dotenv_path=Path(__file__).resolve().parents[1] / ".env"
)

# --------------------------------------------------
# Configure Gemini
# --------------------------------------------------

def configure_gemini():
    """
    Configure Gemini using GOOGLE_API_KEY.
    """

    if not GENAI_AVAILABLE:
        raise ImportError(
            "Failed to import google.generativeai.\n"
            "Check the terminal output above for the real error."
        )

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file."
        )

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("gemini-2.5-flash")

# --------------------------------------------------
# Build Prompt
# --------------------------------------------------

def build_prompt(query, retrieved_docs):
    """
    Build prompt using retrieved documents.
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

# --------------------------------------------------
# Generate Answer
# --------------------------------------------------

def generate_answer(query, retrieved_docs):
    """
    Generate answer using Gemini.
    """

    try:
        print("===== DEBUG START =====")

        model = configure_gemini()
        print("✅ Gemini model configured")

        prompt = build_prompt(query, retrieved_docs)
        print("✅ Prompt built")

        response = model.generate_content(prompt)
        print("✅ Response received")

        print("===== DEBUG END =====")

        return response.text

    except Exception as e:
        import traceback

        print("\n\n========== REAL ERROR ==========")
        traceback.print_exc()
        print("================================\n\n")

        raise e