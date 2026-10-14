# MedLearn: Continuous Medical Paper Learning Web App

## Overview
This repository implements the **MVP** of a web application that helps primary‑care, family‑medicine, home‑care, and related clinicians stay up‑to‑date with the latest clinically relevant English medical papers.

- **Backend** – FastAPI (Python) with SQLite (SQLAlchemy). Handles:
  - PubMed / Europe PMC retrieval (last 6 months, English only)
  - Scoring and selection of a single *Today's Paper*
  - Related papers, user feedback, tomorrow‑topic storage
  - Simple gamification (learning streak, XP counters)
- **Frontend** – React (TypeScript) built with Vite. Displays:
  - Greeting and the *Today's Paper* with Japanese recommendation reason
  - English paper summary, clinical question, methods, key results, take‑away, limitations, reflection prompt
  - Related papers and “You may also like” section
  - Input box for tomorrow’s topic
  - Feedback buttons (Interesting, Not relevant, Already knew, Save, Read full paper)
  - Learning‑streak badge
- **Configuration** – Secrets (PubMed API key, optional) are read from an `.env` file; never committed to source.

The code is deliberately modular so that additional features (XP/Level system, Knowledge Map, weekly summary, etc.) can be added later without touching core logic.

## Project Structure
```
medlearn_app/
├─ backend/               # FastAPI server
│   ├─ main.py            # app entry point
│   ├─ database.py        # DB engine & session
│   ├─ models.py          # SQLAlchemy models
│   ├─ schemas.py         # Pydantic request/response schemas
│   ├─ pubmed_client.py   # PubMed / Europe PMC wrapper
│   ├─ recommender.py     # Recommendation scoring (MVP stub)
│   └─ routers/
│        └─ papers.py      # API routes used by UI
├─ frontend/              # React UI
│   ├─ src/
│   │   ├─ App.tsx        # Main layout
│   │   ├─ components/
│   │   │   ├─ TodayPaper.tsx
│   │   │   ├─ RelatedPapers.tsx
│   │   │   └─ FeedbackButtons.tsx
│   │   └─ api.ts         # thin wrapper around fetch calls
│   ├─ public/
│   ├─ index.html
│   └─ package.json
├─ .env.example          # Example environment variables
├─ requirements.txt       # Python deps for backend
└─ README.md               # this file
```

## Getting Started (local development)
1. **Create a workspace** – The project lives under the Antigravity scratch directory. Set it as the active workspace:
   ```
   cd /Users/masahiro-takakuwa/.gemini/antigravity/scratch/medlearn_app
   ```
2. **Backend**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   # copy .env.example → .env and fill PubMed API key if you have one
   uvicorn backend.main:app --reload
   ```
3. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev   # Vite dev server, typically http://localhost:5173
   ```
4. Open the UI in a browser – the frontend talks to `http://localhost:8000` (FastAPI) for data.

---
### Next Steps (post‑MVP)
- Implement full gamification (XP, Levels, Knowledge Map)
- Add weekly learning‑summary endpoint & UI
- Persist user accounts (OAuth / email) instead of a single‑user SQLite file
- Switch to PostgreSQL for scalability
- Deploy to a cloud platform (Docker, Cloud Run, etc.)

Feel free to dive into any module; the code contains inline TODOs where the full logic will be expanded later.
