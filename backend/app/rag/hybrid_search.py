from rank_bm25 import BM25Okapi

from app.rag.chroma_store import semantic_search
from app.rag.knowledge_base.seed_data import KNOWLEDGE_CHUNKS

_bm25 = None
_bm25_ids = None


def _get_bm25():
    global _bm25, _bm25_ids
    if _bm25 is None:
        corpus = [c["text"] for c in KNOWLEDGE_CHUNKS]
        _bm25_ids = [c["id"] for c in KNOWLEDGE_CHUNKS]
        tokenized = [doc.lower().split() for doc in corpus]
        _bm25 = BM25Okapi(tokenized)
    return _bm25, _bm25_ids


def _bm25_search(query: str, k: int = 4) -> list[str]:
    bm25, ids = _get_bm25()
    scores = bm25.get_scores(query.lower().split())
    ranked = sorted(zip(ids, scores), key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, _ in ranked[:k]]


def hybrid_retrieve(query: str, k: int = 4, rrf_k: int = 60) -> list[dict]:
    """Combine BM25 (keyword) and semantic (embedding) rankings via
    Reciprocal Rank Fusion, so results strong in either exact terminology
    or conceptual similarity both surface.
    """
    semantic_hits = semantic_search(query, n_results=k)
    semantic_rank = {hit["id"]: i for i, hit in enumerate(semantic_hits)}
    bm25_rank = {doc_id: i for i, doc_id in enumerate(_bm25_search(query, k=k))}

    all_ids = set(semantic_rank) | set(bm25_rank)
    fused_scores = {}
    for doc_id in all_ids:
        score = 0.0
        if doc_id in semantic_rank:
            score += 1.0 / (rrf_k + semantic_rank[doc_id] + 1)
        if doc_id in bm25_rank:
            score += 1.0 / (rrf_k + bm25_rank[doc_id] + 1)
        fused_scores[doc_id] = score

    id_to_chunk = {c["id"]: c for c in KNOWLEDGE_CHUNKS}
    ranked_ids = sorted(fused_scores, key=lambda i: fused_scores[i], reverse=True)[:k]
    return [
        {"id": i, "text": id_to_chunk[i]["text"], "domain": id_to_chunk[i]["domain"],
         "score": fused_scores[i]}
        for i in ranked_ids
    ]
