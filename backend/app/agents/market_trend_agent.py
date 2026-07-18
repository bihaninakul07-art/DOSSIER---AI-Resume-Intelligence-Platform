import logging

from app.models.schemas import ExtractedProfile

logger = logging.getLogger(__name__)


async def run_market_trend_agent(profile: ExtractedProfile) -> list[str]:
    """Live web search for current in-demand skills in the candidate's
    domain. Degrades gracefully (returns an empty list) if the search
    backend is unavailable - the pipeline should never hard-fail here.
    """
    query = f"in-demand skills {profile.primary_domain} engineer 2026"
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return [r.get("body", "")[:300] for r in results if r.get("body")]
    except Exception as e:
        logger.warning("Market trend search failed (%s), continuing without it", e)
        return []
