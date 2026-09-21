"""
DocMind AI
----------
Upload a PDF or a scanned image (screenshot, photo of a page, etc.),
and ask questions about it in plain English. The app extracts the
text itself (OCR for images) and uses Claude to answer questions
grounded only in that document.

Run locally with:
    streamlit run app.py
"""

import streamlit as st
from utils.extractor import extract_text
from utils.ai_client import ask_question, summarize_document

st.set_page_config(page_title="DocMind AI", page_icon="📄", layout="centered")

# ---------- Sidebar: API key + info ----------
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get one free at aistudio.google.com/apikey. Never shared or stored.",
    )
    st.markdown("---")
    st.markdown(
        "**DocMind AI**\n\n"
        "Upload a PDF or image, then ask questions about its content. "
        "Built with Streamlit, pypdf/pytesseract for extraction, "
        "and the Google Gemini API for answers."
    )

st.title("📄 DocMind AI")
st.caption("Upload a document. Ask it anything.")

# ---------- Session state setup ----------
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (question, answer) tuples
if "file_name" not in st.session_state:
    st.session_state.file_name = ""

# ---------- File upload ----------
uploaded_file = st.file_uploader(
    "Upload a PDF or image (PNG/JPG)", type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file is not None and uploaded_file.name != st.session_state.file_name:
    with st.spinner("Extracting text from your document..."):
        try:
            extracted = extract_text(uploaded_file)
        except Exception as e:
            st.error(f"Couldn't extract text: {e}")
            extracted = ""

    if not extracted:
        st.warning(
            "No readable text was found. If this is a scanned image, make sure "
            "it's clear and well-lit; if it's a PDF, it may be a pure image-scan "
            "PDF with no embedded text layer."
        )
    else:
        st.session_state.document_text = extracted
        st.session_state.file_name = uploaded_file.name
        st.session_state.chat_history = []  # reset chat for a new document
        st.success(f"Extracted {len(extracted)} characters from {uploaded_file.name}")

# ---------- Show extracted text + summary option ----------
if st.session_state.document_text:
    with st.expander("View extracted text"):
        st.text_area("Extracted content", st.session_state.document_text, height=200)

    if st.button("Summarize this document"):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar first.")
        else:
            with st.spinner("Summarizing..."):
                try:
                    summary = summarize_document(api_key, st.session_state.document_text)
                    st.info(summary)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    st.markdown("---")
    st.subheader("Ask a question about this document")

    question = st.text_input("Your question", key="question_input")

    if st.button("Ask") and question:
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = ask_question(api_key, st.session_state.document_text, question)
                    st.session_state.chat_history.append((question, answer))
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    # ---------- Chat history ----------
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("Conversation")
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"**You:** {q}")
            st.markdown(f"**DocMind AI:** {a}")
            st.markdown("")
else:
    st.info("Upload a PDF or image above to get started.")
