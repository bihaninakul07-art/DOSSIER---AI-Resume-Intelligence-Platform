from fastapi import APIRouter, HTTPException

from app.memory.session_store import list_history, get_analysis

router = APIRouter()


@router.get("/history")
async def get_history():
    return {"items": list_history()}


@router.get("/history/{session_id}")
async def get_session(session_id: str):
    result = get_analysis(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    return result
