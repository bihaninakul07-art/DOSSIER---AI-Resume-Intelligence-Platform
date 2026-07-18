import json
import os
import sqlite3
import time
import uuid
from contextlib import contextmanager

DB_PATH = os.getenv("SQLITE_PATH", "/tmp/resume_analyzer.db")


@contextmanager
def _conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                session_id TEXT PRIMARY KEY,
                created_at REAL,
                result_json TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS followups (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                question TEXT,
                answer TEXT,
                created_at REAL
            )
        """)


def new_session_id() -> str:
    return str(uuid.uuid4())


def save_analysis(session_id: str, result: dict):
    with _conn() as c:
        c.execute(
            "INSERT OR REPLACE INTO analyses (session_id, created_at, result_json) VALUES (?, ?, ?)",
            (session_id, time.time(), json.dumps(result)),
        )


def get_analysis(session_id: str) -> dict | None:
    with _conn() as c:
        row = c.execute(
            "SELECT result_json FROM analyses WHERE session_id = ?", (session_id,)
        ).fetchone()
    return json.loads(row[0]) if row else None


def list_history(limit: int = 20) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT session_id, created_at, result_json FROM analyses "
            "ORDER BY created_at DESC LIMIT ?", (limit,),
        ).fetchall()
    return [
        {"session_id": r[0], "created_at": r[1], "result": json.loads(r[2])}
        for r in rows
    ]


def save_followup(session_id: str, question: str, answer: str):
    with _conn() as c:
        c.execute(
            "INSERT INTO followups (id, session_id, question, answer, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), session_id, question, answer, time.time()),
        )


def get_followups(session_id: str) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT question, answer, created_at FROM followups "
            "WHERE session_id = ? ORDER BY created_at ASC", (session_id,),
        ).fetchall()
    return [{"question": r[0], "answer": r[1], "created_at": r[2]} for r in rows]
