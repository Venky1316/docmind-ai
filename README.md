# DocMind AI 📄🤖

An AI-powered document assistant. Upload a PDF or a photo/screenshot of a
page, and ask questions about it in plain English — DocMind AI extracts
the text (using OCR for images) and answers your questions using Claude.

**Tech stack:** Python · Streamlit · pypdf · pytesseract (OCR) · Anthropic API

---

## 1. What this project demonstrates (for your portfolio/resume)

- Building and deploying a real Streamlit web app
- Document text extraction (PDF parsing + OCR on images)
- Integrating a Generative AI API (Anthropic Claude) into a product
- Managing app state (session state, chat history) in Streamlit
- Clean project structure: separating UI, extraction logic, and AI logic

---

## 2. Project structure

```
docmind-ai/
├── app.py                # Main Streamlit app (UI + flow)
├── requirements.txt      # Python dependencies
├── .gitignore
├── README.md
└── utils/
    ├── __init__.py
    ├── extractor.py       # PDF/image text extraction
    └── ai_client.py       # Anthropic API wrapper
```

---

## 3. Run it locally (step by step)

### Step 1 — Install Tesseract OCR (needed for image uploads)

pytesseract is just a Python wrapper — it needs the actual Tesseract
engine installed on your machine.

**On macOS** (you're on a MacBook, so use this):
```bash
brew install tesseract
```

**On Windows:** download the installer from
https://github.com/UB-Mannheim/tesseract/wiki and add it to your PATH.

**On Linux (Debian/Ubuntu):**
```bash
sudo apt-get install tesseract-ocr
```

### Step 2 — Set up a virtual environment

```bash
cd docmind-ai
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
```

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Get an Anthropic API key

Go to https://console.anthropic.com, sign in, and create an API key.
You'll paste this into the app's sidebar when it runs (it is never
saved to disk).

### Step 5 — Run the app

```bash
streamlit run app.py
```

This opens the app in your browser at `http://localhost:8501`.
Paste your API key into the sidebar, upload a PDF or image, and start
asking questions.

---

## 4. Push it to GitHub

```bash
cd docmind-ai
git init
git add .
git commit -m "Initial commit: DocMind AI"
git branch -M main
git remote add origin https://github.com/<your-username>/docmind-ai.git
git push -u origin main
```

(Replace `<your-username>` with your GitHub username — e.g. Venky1316,
matching your other repos.)

---

## 5. Deploy it as a live website (Streamlit Community Cloud)

This is the same platform you used for SkillGap AI.

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **"New app"**.
3. Select the `docmind-ai` repository, branch `main`, and file `app.py`.
4. Click **Deploy**.
5. Your app will be live at a URL like:
   `https://docmind-ai-<random>.streamlit.app`

**Important:** Streamlit Community Cloud's default servers don't have
Tesseract pre-installed. To make OCR work in the cloud, add a file
named `packages.txt` (no extension) in the project root with this
single line:
```
tesseract-ocr
```
Streamlit Cloud reads this file and installs system-level packages
automatically before starting your app.

---

## 6. Ideas to extend it further (good for interview talking points)

- Support multi-file upload and let users ask questions across several
  documents at once.
- Add a "Download conversation as PDF" export button.
- Cache extracted text so re-uploading the same file doesn't reprocess it.
- Add authentication so each user's documents/API key stay private.
- Swap Anthropic for a local open-source model to make it fully free to run.

---

## 7. Troubleshooting

| Problem | Likely fix |
|---|---|
| `TesseractNotFoundError` | Tesseract isn't installed or not on PATH — redo Step 1 |
| "No readable text was found" | The PDF might be a scanned image with no text layer, or the image is too blurry for OCR |
| API errors when asking a question | Check your API key is correct and has available credits |
| App works locally but OCR fails on Streamlit Cloud | Make sure `packages.txt` with `tesseract-ocr` is in the repo root |
