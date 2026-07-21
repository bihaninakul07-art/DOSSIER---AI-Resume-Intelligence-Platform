"""Poster generation via Pollinations.ai - keyless, free, FLUX-backed.
NVIDIA's free-tier image endpoints are inconsistent/model-specific, so
this avoids that entirely instead of fighting bespoke invoke URLs.
"""
import base64
import logging
import urllib.parse

import requests

from app.models.schemas import Recommendation

logger = logging.getLogger(__name__)

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"


def _build_prompt(recommendation: Recommendation) -> str:
    top_skills = ", ".join(recommendation.skills_to_learn[:3]) or "career growth"
    top_project = (recommendation.project_ideas[0] if recommendation.project_ideas
                   else "a portfolio project")
    return (
        f"A clean, modern infographic-style poster titled 'Career Roadmap', "
        f"minimalist flat design, showing a growth path with icons for "
        f"{top_skills}, and a highlighted milestone for '{top_project}', "
        f"professional color palette of blue and teal, vector illustration style"
    )


async def generate_poster(recommendation: Recommendation) -> str | None:
    prompt = _build_prompt(recommendation)
    url = POLLINATIONS_URL.format(prompt=urllib.parse.quote(prompt))
    try:
        resp = requests.get(url, params={"width": 1024, "height": 1024, "nologo": "true"}, timeout=60)
        resp.raise_for_status()
        b64 = base64.b64encode(resp.content).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        logger.warning("Poster generation failed: %s", e)
        return None
