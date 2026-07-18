from app.rag.hybrid_search import hybrid_retrieve
from app.models.schemas import ExtractedProfile, RetrievedContext


async def run_rag_agent(profile: ExtractedProfile) -> list[RetrievedContext]:
    query = f"{profile.primary_domain} engineer skills projects " + " ".join(profile.skills[:8])
    hits = hybrid_retrieve(query, k=4)
    return [
        RetrievedContext(source_id=h["id"], text=h["text"], domain=h["domain"])
        for h in hits
    ]
