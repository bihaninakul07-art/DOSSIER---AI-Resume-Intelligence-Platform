"""Poster generation via Pollinations.ai - keyless, free, FLUX-backed.
NVIDIA's free-tier image endpoints are inconsistent/model-specific, so
this avoids that entirely instead of fighting bespoke invoke URLs.

Text is never requested from the image model (diffusion models reliably
garble rendered text) - instead we generate a clean text-free background/
illustration, then overlay real, legible text on top with Pillow.
"""
import base64
import io
import logging
import urllib.parse

import requests
from PIL import Image, ImageDraw, ImageFont

from app.models.schemas import Recommendation

logger = logging.getLogger(__name__)

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"


def _build_prompt(recommendation: Recommendation) -> str:
    top_skills = ", ".join(recommendation.skills_to_learn[:3]) or "career growth"
    return (
        f"A clean, modern infographic-style background, minimalist flat design, "
        f"abstract growth path with icons representing {top_skills}, "
        f"professional color palette of blue and teal, vector illustration style, "
        f"no text, no words, no letters, no typography"
    )


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _overlay_text(image_bytes: bytes, recommendation: Recommendation) -> bytes:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = img.size
    margin = int(width * 0.06)

    title_font = _load_font(int(width * 0.055))
    label_font = _load_font(int(width * 0.028))

    title_h = int(height * 0.12)
    draw.rectangle([0, 0, width, title_h], fill=(15, 30, 45, 190))
    draw.text((margin, title_h * 0.28), "Career Roadmap", font=title_font, fill=(255, 255, 255, 255))

    top_skills = recommendation.skills_to_learn[:3] or ["Career growth"]
    top_project = recommendation.project_ideas[0] if recommendation.project_ideas else "A portfolio project"

    y = title_h + int(height * 0.05)
    draw.text((margin, y), "Skills to learn:", font=label_font, fill=(20, 40, 60, 255))
    y += int(height * 0.045)
    for skill in top_skills:
        for line in _wrap_text(draw, f"- {skill}", label_font, width - 2 * margin):
            draw.text((margin, y), line, font=label_font, fill=(30, 60, 90, 255))
            y += int(height * 0.04)

    y += int(height * 0.03)
    draw.text((margin, y), "Milestone project:", font=label_font, fill=(20, 40, 60, 255))
    y += int(height * 0.045)
    for line in _wrap_text(draw, top_project, label_font, width - 2 * margin):
        draw.text((margin, y), line, font=label_font, fill=(30, 60, 90, 255))
        y += int(height * 0.04)

    combined = Image.alpha_composite(img, overlay).convert("RGB")
    out = io.BytesIO()
    combined.save(out, format="PNG")
    return out.getvalue()


async def generate_poster(recommendation: Recommendation) -> str | None:
    prompt = _build_prompt(recommendation)
    url = POLLINATIONS_URL.format(prompt=urllib.parse.quote(prompt))
    try:
        resp = requests.get(
            url,
            params={"width": 1024, "height": 1024, "nologo": "true", "model": "flux"},
            timeout=60,
        )
        resp.raise_for_status()
        final_bytes = _overlay_text(resp.content, recommendation)
        b64 = base64.b64encode(final_bytes).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        logger.warning("Poster generation failed: %s", e)
        return None
