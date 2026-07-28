import asyncio
import logging

from app.ai.rag.vector_store import VectorMatch, VectorStore
from app.core.config import settings

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        import chromadb

        _client = chromadb.PersistentClient(path=settings.vector_db_persist_dir)
    return _client


class ChromaStore(VectorStore):
    provider_id = "chroma"

    async def upsert(
        self,
        collection_name: str,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        def _run() -> None:
            client = _get_client()
            collection = client.get_or_create_collection(collection_name)
            collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

        await asyncio.to_thread(_run)

    async def query(
        self, collection_name: str, query_embedding: list[float], top_k: int
    ) -> list[VectorMatch]:
        def _run() -> list[VectorMatch]:
            client = _get_client()
            collection = client.get_or_create_collection(collection_name)
            count = collection.count()
            if count == 0:
                return []
            result = collection.query(query_embeddings=[query_embedding], n_results=min(top_k, count))
            ids = result["ids"][0]
            documents = result["documents"][0]
            metadatas = result["metadatas"][0]
            distances = result["distances"][0]
            return [
                VectorMatch(
                    id=ids[i],
                    document=documents[i],
                    metadata=metadatas[i] or {},
                    score=1.0 / (1.0 + distances[i]),
                )
                for i in range(len(ids))
            ]

        return await asyncio.to_thread(_run)

    async def delete_collection(self, collection_name: str) -> None:
        def _run() -> None:
            client = _get_client()
            try:
                client.delete_collection(collection_name)
            except Exception:
                logger.warning("Failed to delete Chroma collection %s", collection_name, exc_info=True)

        await asyncio.to_thread(_run)
