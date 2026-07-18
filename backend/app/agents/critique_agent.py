import json
import logging

from app.llm.router import llm_router
from app.models.schemas import ExtractedProfile, RetrievedContext, GapAnalysis

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a rigorous technical hiring critique engine. Compare the "
    "candidate profile against the retrieved role benchmarks and market "
    "signals, then identify concrete gaps and strengths. Respond ONLY with "
    "JSON matching: {\"missing_skills\": [string], \"weak_sections\": [string], "
    "\"strengths\": [string], \"reasoning\": string (2-3 sentences)}. "
    "No prose outside the JSON."
)


async def run_critique_agent(
    profile: ExtractedProfile,
    context: list[RetrievedContext],
    market_notes: list[str],
) -> GapAnalysis:
    context_text = "\n".join(f"- {c.text}" for c in context)
    market_text = "\n".join(f"- {m}" for m in market_notes) or "(no live market data available)"

    prompt = (
        f"Candidate profile:\n{profile.model_dump_json()}\n\n"
        f"Retrieved role benchmarks:\n{context_text}\n\n"
        f"Current market signals:\n{market_text}"
    )

    result = await llm_router.generate(
        task="critique",
        prompt=prompt,
        system=SYSTEM_PROMPT,
        json_mode=True,
        temperature=0.3,
        max_tokens=1000,
    )
    try:
        data = json.loads(result.text)
        return GapAnalysis(**data)
    except Exception as e:
        logger.warning("Critique JSON parse failed (%s), using fallback", e)
        return GapAnalysis(reasoning="Analysis could not be fully parsed; see raw output.")
