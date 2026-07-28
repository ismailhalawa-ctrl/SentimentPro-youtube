from app.ai.rag.vector_store import VectorStore
from app.core.config import settings

_instance: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _instance
    if _instance is None:
        _instance = _build(settings.vector_db_provider)
    return _instance


def _build(provider_id: str) -> VectorStore:
    if provider_id == "qdrant":
        from app.ai.rag.qdrant_store import QdrantStore

        return QdrantStore()
    if provider_id == "pinecone":
        from app.ai.rag.pinecone_store import PineconeStore

        return PineconeStore()
    from app.ai.rag.chroma_store import ChromaStore

    return ChromaStore()
