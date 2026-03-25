# Spacewind

**Spacewind** is a self-hosted AI and Generative AI studio, accessible at [spacewind.xyz](http://spacewind.xyz). The site is served directly from an Ubuntu laptop and acts as both a personal portfolio and an active playground for AI/GenAI experiments.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup & Running](#setup--running)
- [Environment Variables](#environment-variables)
- [Feature Flags](#feature-flags)
- [API Reference](#api-reference)
- [Notes](#notes)

---

## Overview

Spacewind combines day-to-day tooling needs with hands-on experimentation in web development, AI, and self-hosting. The tagline sums it up: **"Ideas at escape velocity."**

Key goals:
- Ship real, working AI tools — not just demos
- Self-host everything to retain full control and learn infrastructure deeply
- Prototype quickly, iterate relentlessly

---

## Project Structure

```
spacewind/
├── main.py                          # Main FastAPI entry point (feature flags live here)
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .gitignore
│
├── main_sapacewind/                 # Primary website
│   ├── backend/
│   │   ├── github_auto_puller.py   # Git auto-pull helper
│   │   ├── webhook/
│   │   │   └── handler.py          # GitHub webhook endpoint (/webhook)
│   │   └── wordtopdf/
│   │       └── converter.py        # DOCX → PDF converter (/convert)
│   ├── frontend/                    # Static site (HTML/CSS/JS)
│   │   ├── index.html
│   │   ├── projects.html
│   │   ├── contact.html
│   │   ├── privacy.html
│   │   ├── terms.html
│   │   ├── cookies.html
│   │   ├── mini_projects.html
│   │   ├── css/styles.css
│   │   ├── js/script.js
│   │   └── assets/
│   └── mini_projects/              # Mounted at /mini_projects
│
├── sheep/                           # SheepBot — document Q&A chatbot
│   ├── backend/main.py             # FastAPI app with Gemini RAG pipeline
│   ├── frontend/                    # Chatbot UI (HTML/CSS/JS)
│   └── chroma_db/                  # ChromaDB persistent storage
│
├── hackathon/                       # Sign language video generator
│   ├── backend/main.py
│   ├── frontend/
│   └── text_to_video/
│       ├── collector.py            # Record webcam sign videos
│       └── generator.py            # Generate video from text
│   └── video_to_text/
│       └── recorder.py             # Hand detection + classification
│
└── rohit/                           # Personal portfolio (served on port 5505)
    ├── index.html
    ├── about.html
    ├── projects.html
    ├── contact.html
    └── style.css
```

---

## Features

### Main Website (`main_sapacewind/`)
- Dark-themed marketing site with glassmorphism design and scroll animations
- Hero section, project showcase, and contact forms (via Web3Forms)
- Browser speech synthesis demo — no data leaves the device
- Responsive layout across desktop and mobile

### SheepBot — Document Chatbot (`sheep/`)
- Upload PDF, DOCX, TXT, JPG/PNG, or XLSX files
- Text extraction via `pdfplumber`, `python-docx`, `pytesseract` (OCR), and `openpyxl`
- Documents are chunked (500 chars) and stored in ChromaDB as vector embeddings
- RAG pipeline: retrieves relevant chunks → sends to Google Gemini 1.5 Flash → returns answer
- Auto-cleanup: documents older than 6 hours are purged hourly
- File listing endpoint with metadata and content previews

### Word-to-PDF Converter
- `POST /convert` accepts a `.docx` upload
- Converts using LibreOffice headless mode
- Returns a download link: `https://spacewind.xyz/converted/{file_id}.pdf`

### GitHub Auto-Puller
- `POST /webhook` listens for GitHub push events
- Pulls latest changes automatically when a push to `main` is detected
- `POST /webhook-direct` available as a fallback

### Portfolio
- Personal portfolio served on port `5505` via Python's built-in HTTP server
- Spawned as a subprocess when `RUN_PORTFOLIO = True`

### Sign Language Video Generator (Hackathon project)
- **Collector**: Records 2-second webcam clips per sign for a training dataset
- **Generator**: Sequences stored sign clips into a video from input text
- **Recognizer**: Real-time hand detection using HSV color space and contour analysis

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI + Uvicorn |
| AI / LLM | Google Gemini 1.5 Flash (`google-generativeai`) |
| Vector DB | ChromaDB (persistent) |
| Document parsing | pdfplumber, python-docx, pytesseract, openpyxl, Pillow |
| PDF conversion | LibreOffice (headless) |
| Frontend | Vanilla HTML5, CSS3 (CSS variables, Grid, Flexbox), ES6 JS |
| OS / Hosting | Ubuntu, self-hosted, custom domain via DNS |
| Vision (hackathon) | OpenCV, NumPy |

---

## Setup & Running

### Prerequisites

- Python 3.9+
- LibreOffice (for the Word-to-PDF converter)
- Tesseract OCR (for image text extraction in SheepBot)
- A Google Gemini API key

### Install

```bash
git clone https://github.com/yourusername/spacewind.git
cd spacewind

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Run the main app

```bash
python3 main.py
# Serves on http://localhost:8000
```

The main app mounts:
- `/` — main website frontend
- `/converted` — static PDF download directory
- `/mini_projects` — mini projects static files

### Run SheepBot separately

```bash
cd sheep/backend
python3 main.py
# API at http://localhost:8000/api
# UI at http://localhost:8000/app
```

### Run the Hackathon backend

```bash
cd hackathon/backend
python3 main.py
# Serves on http://localhost:8700
```

---

## Environment Variables

Copy `.env.example` to `.env` before running:

| Variable | Description | Required by |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | SheepBot (`sheep/backend/main.py`) |

---

## Feature Flags

In `main.py`, three boolean flags control which modules are loaded at startup:

```python
RUN_WORDTOPDF = True   # Enables /convert endpoint and /converted static mount
RUN_FRONTEND  = True   # Serves the main website and registers the /webhook endpoint
RUN_PORTFOLIO = True   # Spawns the portfolio HTTP server on port 5505
```

Set any flag to `False` to disable that module without touching any other code.

---

## API Reference

### Word-to-PDF

| Method | Path | Description |
|---|---|---|
| `POST` | `/convert` | Upload a `.docx` file, get back a PDF download link |

### GitHub Webhook

| Method | Path | Description |
|---|---|---|
| `POST` | `/webhook` | GitHub push event handler — pulls main branch |
| `POST` | `/webhook-direct` | Fallback direct pull endpoint |

### SheepBot

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/upload/` | Upload a document (PDF, DOCX, TXT, image, Excel) |
| `POST` | `/api/query/?question=...` | Ask a question against uploaded documents |
| `GET`  | `/api/files/` | List all uploaded files with metadata and chunk count |

---

## Notes

- **Availability**: The site is self-hosted on a laptop — it may be offline if the machine is off or sleeping.
- **CORS**: Currently set to `allow_origins=["*"]` for development convenience. Restrict this in production.
- **Webhook repo path**: `main_sapacewind/backend/webhook/handler.py` has the repo path hardcoded to `/home/rohit/work/github/spacewind`. Update this if the deployment path changes.
- **SheepBot data**: ChromaDB data persists in `sheep/chroma_db/`. Documents auto-expire after 6 hours.
- **Scyther & Lawkar**: These are planned projects — currently placeholder directories.
