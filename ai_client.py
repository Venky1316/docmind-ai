"""
ai_client.py
------------
Thin wrapper around the Anthropic API so app.py doesn't need to know
the details of prompt construction. Swap this file out if you ever
want to point the project at a different provider (e.g. OpenAI) --
the rest of the app doesn't need to change.
"""

import anthropic

MODEL = "claude-sonnet-4-5-20250929"
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
    """Send the document + question to Claude and return the answer text."""
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": build_prompt(document_text, question)}
        ],
    )

    # response.content is a list of content blocks; join any text blocks
    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()


def summarize_document(api_key: str, document_text: str) -> str:
    """Convenience helper: ask for a short summary of the whole document."""
    return ask_question(
        api_key,
        document_text,
        "Summarize this document in 4-6 sentences, covering the key points.",
    )
