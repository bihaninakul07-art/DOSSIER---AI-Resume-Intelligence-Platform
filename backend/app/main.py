import logging

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.memory.session_store import init_db
from app.api import analyze, history, followup

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Resume Intelligence Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to the deployed frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(analyze.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(followup.router, prefix="/api")
