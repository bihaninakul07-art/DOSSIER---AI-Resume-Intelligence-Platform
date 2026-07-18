# DOSSIER — AI Resume Intelligence Platform

An agentic resume analyzer: upload a PDF, and a multi-agent pipeline parses it,
retrieves grounded role/skill benchmarks via RAG, checks live market signals,
critiques the profile against that evidence, and issues a structured career
report — plus a generated "career roadmap" poster image.

Built as a bootcamp capstone to demonstrate: LLM API integration, prompt
engineering, RAG, agentic workflows, multi-agent orchestration, multi-LLM
routing, image generation, memory, and streaming — see `ARCHITECTURE.md`
for the full concept-to-implementation mapping.

## Stack
- **Backend:** FastAPI, LangGraph, ChromaDB + fastembed (hybrid BM25 +
  semantic RAG), Groq + NVIDIA NIM behind a single unified LLM router,
  NVIDIA NIM FLUX for image generation, SQLite for session memory,
  Server-Sent Events for live agent status streaming.
- **Frontend:** Next.js (App Router) + Tailwind, streams the SSE feed to
  show live agent progress, then renders the report, poster, and a
  follow-up Q&A panel grounded in the analysis.

## Run locally

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY, NVIDIA_NIM_API_KEY, NVIDIA_API_KEY
uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000`. `/docs` has the interactive API.

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```
Frontend runs at `http://localhost:3000`.

## API keys
- `GROQ_API_KEY` — free at console.groq.com, used for fast parsing/extraction
- `NVIDIA_NIM_API_KEY` — free at build.nvidia.com, used for deeper critique/recommendation + FLUX poster generation

At least one of GROQ/NVIDIA_NIM must be set; the router falls back to whichever is configured.

## Deploy on Render
This repo includes `render.yaml` defining two services:
1. Push this repo to GitHub.
2. In Render: **New → Blueprint**, point it at the repo — it reads `render.yaml`
   and creates `dossier-backend` (Docker web service) and `dossier-frontend` (Node web service).
3. Set `GROQ_API_KEY`, `NVIDIA_NIM_API_KEY`, `NVIDIA_API_KEY` on the backend service in the Render dashboard.
4. Once the backend deploys, copy its URL (e.g. `https://dossier-backend.onrender.com`)
   into the frontend service's `NEXT_PUBLIC_API_URL` env var, then redeploy the frontend.

## Known limitations
- Free-tier Render services spin down on inactivity — first request after idle will be slow.
- ChromaDB and SQLite persist to a Render disk mount; on the free plan without a disk, data resets on redeploy.
- Market trend search (DuckDuckGo) has no API key requirement but can rate-limit under heavy use — the pipeline degrades gracefully (continues without live market data) if it fails.
- Poster generation is skipped (not failed) if NVIDIA API keys are unset or the NIM endpoint is cold/unavailable.

## Demo video
_(add link here)_