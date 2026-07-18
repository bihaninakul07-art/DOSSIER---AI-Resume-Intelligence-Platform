import os
import chromadb

from app.rag.embeddings import embed_texts
from app.rag.knowledge_base.seed_data import KNOWLEDGE_CHUNKS

_COLLECTION_NAME = "resume_knowledge_base"
_PERSIST_DIR = os.getenv("CHROMA_DIR", "/tmp/chroma_data")

_client = None
_collection = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=_PERSIST_DIR)
    return _client


def get_collection():
    global _collection
    if _collection is not None:
        return _collection

    client = _get_client()
    collection = client.get_or_create_collection(name=_COLLECTION_NAME)

    if collection.count() == 0:
        texts = [c["text"] for c in KNOWLEDGE_CHUNKS]
        ids = [c["id"] for c in KNOWLEDGE_CHUNKS]
        metadatas = [{"domain": c["domain"]} for c in KNOWLEDGE_CHUNKS]
        embeddings = embed_texts(texts)
        collection.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)

    _collection = collection
    return _collection


def semantic_search(query: str, n_results: int = 4) -> list[dict]:
    collection = get_collection()
    query_embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    out = []
    for i in range(len(results["ids"][0])):
        out.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "domain": results["metadatas"][0][i].get("domain"),
            "distance": results["distances"][0][i],
        })
    return out
