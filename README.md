# Spacewind

Self-hosted AI and GenAI studio at [spacewind.xyz](http://spacewind.xyz) — built backend-first on **FastAPI**, with a RAG pipeline, document processing APIs, and a GitHub CI webhook, all served from an Ubuntu laptop.

---

## Backend Architecture

The core is a single FastAPI app (`main.py`) that conditionally mounts routers and static directories based on feature flags. Each sub-feature lives in its own module with its own router, keeping the entry point clean.

```
main.py                          ← FastAPI app, feature flags, subprocess management
main_sapacewind/backend/
  webhook/handler.py             ← POST /webhook  (GitHub push → git pull)
  wordtopdf/converter.py         ← POST /convert  (DOCX → PDF via LibreOffice)
  github_auto_puller.py          ← git pull helper used by both webhook routes
sheep/backend/main.py            ← Standalone FastAPI app: RAG pipeline + document APIs
```

### RAG Pipeline (SheepBot)

`sheep/backend/main.py` implements a full Retrieval-Augmented Generation loop:

1. **Ingest** — `POST /api/upload/` accepts PDF, DOCX, TXT, JPG/PNG, XLSX. Text is extracted per format, chunked at 500 characters, and stored in ChromaDB with a Unix timestamp.
2. **Retrieve** — `POST /api/query/` embeds the question, queries ChromaDB for the top-3 relevant chunks, and builds a context string.
3. **Generate** — context + question are sent to **Gemini 1.5 Flash**; the answer is streamed back as JSON.
4. **Expire** — a background task runs every hour and deletes any document chunks older than 6 hours.

### Document Processing

Each file type has a dedicated extractor:

| Format | Library |
|---|---|
| PDF | pdfplumber |
| DOCX | python-docx |
| TXT | stdlib |
| JPG / PNG | Pillow + pytesseract (OCR) |
| XLS / XLSX | openpyxl |

### Word-to-PDF Converter

`POST /convert` saves the upload to a UUID-named temp file, shells out to `libreoffice --headless --convert-to pdf`, then serves the result from the `/converted` static mount. The UUID filename prevents collisions and avoids exposing the original filename in the download URL.

### GitHub Webhook / Auto-Puller

`POST /webhook` validates the `ref` against `refs/heads/main`, then runs `git pull` in the repo directory via `subprocess`. A fallback route `POST /webhook-direct` calls the same puller directly, bypassing the webhook handler class.

### Feature Flags

Three booleans at the top of `main.py` control which modules load at startup — no config files needed:

```python
RUN_WORDTOPDF = True   # mounts /convert router + /converted static dir
RUN_FRONTEND  = True   # serves frontend static files + registers /webhook
RUN_PORTFOLIO = True   # spawns portfolio HTTP server on port 5505
```

### API Reference

**Main app**

| Method | Path | Description |
|---|---|---|
| `POST` | `/convert` | Upload `.docx`, returns PDF download link |
| `POST` | `/webhook` | GitHub push handler — pulls main branch |
| `POST` | `/webhook-direct` | Fallback direct pull |

**SheepBot** (`sheep/backend/main.py`)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/upload/` | Ingest a document into ChromaDB |
| `POST` | `/api/query/?question=...` | RAG query against stored documents |
| `GET`  | `/api/files/` | List documents with chunk count and preview |

---

## Project Structure

```
spacewind/
├── main.py
├── requirements.txt
├── .env.example
│
├── main_sapacewind/
│   ├── backend/
│   │   ├── github_auto_puller.py
│   │   ├── webhook/handler.py
│   │   └── wordtopdf/converter.py
│   ├── frontend/                    # Static site (HTML/CSS/JS)
│   └── mini_projects/
│
├── sheep/
│   ├── backend/main.py             # RAG pipeline + document APIs
│   ├── frontend/                    # Chatbot UI
│   └── chroma_db/                  # ChromaDB persistent storage
│
├── hackathon/                       # Sign language video generator
│   ├── backend/main.py
│   ├── text_to_video/
│   │   ├── collector.py            # Record webcam sign clips
│   │   └── generator.py            # Sequence clips into video from text
│   └── video_to_text/
│       └── recorder.py             # HSV-based hand detection
│
└── rohit/                           # Portfolio (port 5505)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI + Uvicorn |
| AI / LLM | Google Gemini 1.5 Flash |
| Vector DB | ChromaDB (persistent) |
| Document parsing | pdfplumber, python-docx, pytesseract, openpyxl, Pillow |
| PDF conversion | LibreOffice headless |
| Frontend | HTML5, CSS3, Vanilla JS |
| Hosting | Ubuntu laptop, self-hosted, custom domain |
| Vision | OpenCV, NumPy |

---

## Setup

### Prerequisites

- Python 3.9+
- LibreOffice (`libreoffice` on PATH)
- Tesseract OCR (`tesseract` on PATH)
- A Google Gemini API key

### Install & configure

```bash
git clone https://github.com/yourusername/spacewind.git
cd spacewind

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

### Run

```bash
# Main app (website + converter + webhook)
python3 main.py

# SheepBot standalone
cd sheep/backend && python3 main.py
```

---

## Environment Variables

| Variable | Used by |
|---|---|
| `GEMINI_API_KEY` | `sheep/backend/main.py` — Gemini RAG pipeline |

---

## Notes

- **Availability**: Self-hosted on a laptop — offline when the machine is sleeping.
- **CORS**: Set to `allow_origins=["*"]` for development. Restrict before exposing to production traffic.
- **Webhook path**: `webhook/handler.py` has the repo path hardcoded to `/home/rohit/work/github/spacewind` — update if your deployment path differs.
- **SheepBot data**: Persists in `sheep/chroma_db/`. Chunks auto-expire after 6 hours.
- **Scyther & Lawkar**: Planned projects — placeholder directories only.
