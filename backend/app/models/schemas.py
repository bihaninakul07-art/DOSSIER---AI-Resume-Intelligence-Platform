from typing import Optional
from pydantic import BaseModel


class ParsedResume(BaseModel):
    raw_text: str
    experience: list[str] = []
    education: list[str] = []
    projects: list[str] = []
    skills_section: Optional[str] = None


class ExtractedProfile(BaseModel):
    skills: list[str] = []
    years_experience: Optional[float] = None
    primary_domain: str = "general"
    seniority: str = "unclear"


class RetrievedContext(BaseModel):
    source_id: str
    text: str
    domain: str


class GapAnalysis(BaseModel):
    missing_skills: list[str] = []
    weak_sections: list[str] = []
    strengths: list[str] = []
    reasoning: str = ""


class Recommendation(BaseModel):
    project_ideas: list[str] = []
    skills_to_learn: list[str] = []
    overall_recommendations: list[str] = []
    grounded_sources: list[str] = []


class AnalysisResult(BaseModel):
    session_id: str
    extracted_profile: ExtractedProfile
    gap_analysis: GapAnalysis
    recommendation: Recommendation
    poster_url: Optional[str] = None
    provider_notes: dict = {}
