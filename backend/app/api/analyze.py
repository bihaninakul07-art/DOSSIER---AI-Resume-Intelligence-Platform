import json
import logging

from fastapi import APIRouter, UploadFile, File
from sse_starlette.sse import EventSourceResponse

from app.agents.supervisor import run_pipeline_streaming
from app.memory.session_store import new_session_id, save_analysis
from app.models.schemas import AnalysisResult, ExtractedProfile, GapAnalysis, Recommendation

logger = logging.getLogger(__name__)
router = APIRouter()

NODE_LABELS = {
    "parser": "Reading resume...",
    "extractor": "Extracting skills & experience...",
    "rag_agent": "Retrieving role benchmarks...",
    "market_trend_agent": "Checking current market trends...",
    "critique": "Analyzing gaps...",
    "recommendation_agent": "Generating recommendations...",
    "poster": "Designing your roadmap poster...",
}


@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    session_id = new_session_id()

    async def event_stream():
        final_state: dict = {}
        try:
            async for node_name, delta in run_pipeline_streaming(pdf_bytes):
                final_state.update(delta)
                yield {
                    "event": "status",
                    "data": json.dumps({
                        "node": node_name,
                        "label": NODE_LABELS.get(node_name, node_name),
                    }),
                }

            profile = final_state.get("profile") or ExtractedProfile()
            gap = final_state.get("gap_analysis") or GapAnalysis()
            rec = final_state.get("recommendation") or Recommendation()

            result = AnalysisResult(
                session_id=session_id,
                extracted_profile=profile,
                gap_analysis=gap,
                recommendation=rec,
                poster_url=final_state.get("poster_url"),
                provider_notes=final_state.get("provider_notes", {}),
            )
            save_analysis(session_id, result.model_dump())

            yield {"event": "complete", "data": result.model_dump_json()}
        except Exception as e:
            logger.exception("Pipeline failed")
            yield {"event": "error", "data": json.dumps({"message": str(e)})}

    return EventSourceResponse(event_stream())
