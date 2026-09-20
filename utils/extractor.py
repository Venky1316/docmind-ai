"""
extractor.py
------------
Handles pulling raw text out of whatever the user uploads:
- PDF files -> extracted page by page with pypdf
- Image files (png/jpg/jpeg) -> extracted with OCR (pytesseract)

Keeping this in its own module means app.py stays clean, and you can
swap out the extraction engine later without touching the UI code.
"""

from io import BytesIO
from pypdf import PdfReader
from PIL import Image
import pytesseract


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from every page of a PDF file.

    uploaded_file: a Streamlit UploadedFile object (behaves like a file handle)
    """
    reader = PdfReader(uploaded_file)
    pages_text = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages_text.append(f"--- Page {i + 1} ---\n{text.strip()}")

    if not pages_text:
        return ""

    return "\n\n".join(pages_text)


def extract_text_from_image(uploaded_file) -> str:
    """Run OCR on an uploaded image and return the recognized text.

    Requires the Tesseract OCR engine to be installed on the machine
    (see README.md for install instructions). pytesseract is just a
    Python wrapper around that binary.
    """
    image = Image.open(uploaded_file)

    # Convert to RGB in case of PNGs with an alpha channel, which can
    # sometimes trip up the OCR engine.
    if image.mode != "RGB":
        image = image.convert("RGB")

    text = pytesseract.image_to_string(image)
    return text.strip()


def extract_text(uploaded_file) -> str:
    """Dispatch to the right extractor based on file type."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {filename}")
