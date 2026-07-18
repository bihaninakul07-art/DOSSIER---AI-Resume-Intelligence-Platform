import json
import logging

from app.llm.router import llm_router
from app.models.schemas import ParsedResume, ExtractedProfile

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a precise resume-data extraction engine. Given raw resume text, "
    "extract structured facts. Respond ONLY with a JSON object matching this "
    "schema: {\"skills\": [string], \"years_experience\": number, "
    "\"primary_domain\": one of ['backend','frontend','ml','devops','general'], "
    "\"seniority\": one of ['entry','mid','senior','unclear']}. "
    "No prose, no markdown fences, JSON only."
)


async def run_extractor(parsed: ParsedResume) -> ExtractedProfile:
    prompt = f"Resume text:\n\n{parsed.raw_text[:6000]}"
    result = await llm_router.generate(
        task="extraction",
        prompt=prompt,
        system=SYSTEM_PROMPT,
        json_mode=True,
        temperature=0.1,
        max_tokens=800,
    )
    try:
        data = json.loads(result.text)
        return ExtractedProfile(**data)
    except Exception as e:
        logger.warning("Extractor JSON parse failed (%s), using fallback", e)
        return ExtractedProfile(
            skills=[],
            years_experience=None,
            primary_domain="general",
            seniority="unclear",
        )
