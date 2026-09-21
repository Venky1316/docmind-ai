"""
ai_client.py
------------
Thin wrapper around the Google Gemini API so app.py doesn't need to know
the details of prompt construction.
"""

import google.generativeai as genai

MODEL = "gemini-3-flash-preview"
MAX_CONTEXT_CHARS = 15000  # keeps requests small & cheap; trims very long docs


def build_prompt(document_text: str, question: str) -> str:
    trimmed = document_text[:MAX_CONTEXT_CHARS]

    return f"""You are a helpful assistant answering questions about a document.
Only use the document content below to answer. If the answer isn't in the
document, say so clearly instead of guessing.

DOCUMENT:
\"\"\"
{trimmed}
\"\"\"

QUESTION: {question}

Answer clearly and concisely."""


def ask_question(api_key: str, document_text: str, question: str) -> str:
    """Send the document + question to Gemini and return the answer text."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)

    response = model.generate_content(build_prompt(document_text, question))

    return response.text.strip()


def summarize_document(api_key: str, document_text: str) -> str:
    """Convenience helper: ask for a short summary of the whole document."""
    return ask_question(
        api_key,
        document_text,
        "Summarize this document in 4-6 sentences, covering the key points.",
    )


