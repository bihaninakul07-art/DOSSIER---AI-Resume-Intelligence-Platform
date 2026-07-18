import json
import logging

from app.llm.router import llm_router
from app.models.schemas import ExtractedProfile, GapAnalysis, RetrievedContext, Recommendation

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a career recommendation engine. Using the candidate profile "
    "and the gap analysis, produce specific, actionable recommendations. "
    "Respond ONLY with JSON: {\"project_ideas\": [string], "
    "\"skills_to_learn\": [string], \"overall_recommendations\": [string]}. "
    "Each list item must be concrete and specific to this candidate, not generic."
)


async def run_recommendation_agent(
    profile: ExtractedProfile,
    gap_analysis: GapAnalysis,
    context: list[RetrievedContext],
) -> tuple[Recommendation, dict]:
    prompt = (
        f"Profile: {profile.model_dump_json()}\n\n"
        f"Gap analysis: {gap_analysis.model_dump_json()}"
    )

    # cross_validate=True: also runs the same task on the other configured
    # provider so we can surface agreement/divergence without a full debate.
    result = await llm_router.generate(
        task="recommendation",
        prompt=prompt,
        system=SYSTEM_PROMPT,
        json_mode=True,
        temperature=0.5,
        max_tokens=1200,
        cross_validate=True,
    )

    try:
        data = json.loads(result.text)
        rec = Recommendation(
            **data,
            grounded_sources=[c.source_id for c in context],
        )
    except Exception as e:
        logger.warning("Recommendation JSON parse failed (%s), using fallback", e)
        rec = Recommendation(grounded_sources=[c.source_id for c in context])

    provider_notes = {
        "primary_provider": result.provider_used,
        "cross_checked": result.cross_check is not None,
    }
    if result.cross_check:
        provider_notes["secondary_provider"] = result.cross_check["provider"]

    return rec, provider_notes
