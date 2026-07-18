from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm.router import llm_router
from app.memory.session_store import get_analysis, save_followup, get_followups

router = APIRouter()

SYSTEM_PROMPT = (
    "You are a helpful career advisor answering a follow-up question about "
    "a resume analysis you already produced. Use the provided analysis "
    "context to answer specifically and concisely (3-5 sentences)."
)


class FollowupRequest(BaseModel):
    session_id: str
    question: str


@router.post("/followup")
async def ask_followup(req: FollowupRequest):
    analysis = get_analysis(req.session_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Session not found")

    prompt = f"Analysis context:\n{analysis}\n\nQuestion: {req.question}"
    result = await llm_router.generate(
        task="recommendation",
        prompt=prompt,
        system=SYSTEM_PROMPT,
        temperature=0.4,
        max_tokens=500,
    )
    save_followup(req.session_id, req.question, result.text)
    return {"answer": result.text}


@router.get("/followup/{session_id}")
async def get_history_for_session(session_id: str):
    return {"items": get_followups(session_id)}
