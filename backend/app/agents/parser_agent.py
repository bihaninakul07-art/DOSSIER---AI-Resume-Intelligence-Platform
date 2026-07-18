import io
import re

from pypdf import PdfReader

from app.models.schemas import ParsedResume

SECTION_HEADERS = {
    "experience": ["experience", "work experience", "employment"],
    "education": ["education", "academic background"],
    "projects": ["projects", "personal projects"],
    "skills": ["skills", "technical skills", "technologies"],
}


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _split_into_sections(raw_text: str) -> dict[str, list[str]]:
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    sections: dict[str, list[str]] = {k: [] for k in SECTION_HEADERS}
    current = None

    for line in lines:
        lower = line.lower()
        matched = None
        for key, headers in SECTION_HEADERS.items():
            if any(re.fullmatch(rf"{h}s?:?", lower) or lower.startswith(h) and len(lower) < len(h) + 4
                   for h in headers):
                matched = key
                break
        if matched:
            current = matched
            continue
        if current:
            sections[current].append(line)

    return sections


def run_parser(pdf_bytes: bytes) -> ParsedResume:
    raw_text = extract_text_from_pdf(pdf_bytes)
    sections = _split_into_sections(raw_text)
    return ParsedResume(
        raw_text=raw_text,
        experience=sections.get("experience", []),
        education=sections.get("education", []),
        projects=sections.get("projects", []),
        skills_section="\n".join(sections.get("skills", [])) or None,
    )
