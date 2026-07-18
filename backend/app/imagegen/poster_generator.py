"""Poster generation using NVIDIA NIM (FLUX) via NvidiaNimImageClient."""
import logging
import os

from app.llm.nvidia_client import NvidiaNimImageClient
from app.models.schemas import Recommendation

logger = logging.getLogger(__name__)


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
    """
    Generate career roadmap poster using NVIDIA NIM FLUX.
    Returns base64 data URL or None if not configured/failed.
    """
    # Check both possible env var names for backward compatibility
    api_key = os.getenv("NVIDIA_NIM_API_KEY") or os.getenv("NVIDIA_API_KEY")
    if not api_key:
        logger.info("No image generation provider configured (need NVIDIA_NIM_API_KEY or NVIDIA_API_KEY)")
        return None

    prompt = _build_prompt(recommendation)
    client = NvidiaNimImageClient()

    if not client.available:
        logger.warning("NvidiaNimImageClient not available")
        return None

    try:
        data_url = await client.generate(prompt)
        if data_url:
            return data_url
        logger.warning("NVIDIA NIM image generation returned no image")
        return None
    except Exception as e:
        logger.warning("Poster generation failed: %s", e)
        return None
    finally:
        await client.close()