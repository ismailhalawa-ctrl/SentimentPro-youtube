import asyncio
import importlib.util
import logging

from app.ai.rag.vector_store import VectorMatch, VectorStore
from app.core.config import settings

logger = logging.getLogger(__name__)

_client = None
_index = None


def _try_import_pinecone() -> bool:
    return importlib.util.find_spec("pinecone") is not None


class PineconeStore(VectorStore):
    provider_id = "pinecone"

    def is_configured(self) -> bool:
        return bool(settings.pinecone_api_key) and _try_import_pinecone()

    def _get_index(self):
        global _client, _index
        if _index is None:
            from pinecone import Pinecone

            _client = Pinecone(api_key=settings.pinecone_api_key)
            _index = _client.Index(settings.pinecone_index_name)
        return _index

    async def upsert(
        self,
        collection_name: str,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        def _run() -> None:
            index = self._get_index()
            vectors = [
                {
                    "id": ids[i],
                    "values": embeddings[i],
                    "metadata": {**metadatas[i], "document": documents[i]},
                }
                for i in range(len(ids))
            ]
            index.upsert(vectors=vectors, namespace=collection_name)

        await asyncio.to_thread(_run)

    async def delete_collection(self, collection_name: str) -> None:
        def _run() -> None:
            index = self._get_index()
            try:
                index.delete(delete_all=True, namespace=collection_name)
            except Exception:
                logger.warning("Failed to delete Pinecone namespace %s", collection_name, exc_info=True)

        await asyncio.to_thread(_run)

    async def query(
        self, collection_name: str, query_embedding: list[float], top_k: int
    ) -> list[VectorMatch]:
        def _run() -> list[VectorMatch]:
            index = self._get_index()
            result = index.query(
                vector=query_embedding, top_k=top_k, namespace=collection_name, include_metadata=True
            )
            matches = []
            for m in result.get("matches", []):
                metadata = dict(m.get("metadata") or {})
                document = metadata.pop("document", "")
                matches.append(
                    VectorMatch(id=m["id"], document=document, metadata=metadata, score=m.get("score", 0.0))
                )
            return matches

        return await asyncio.to_thread(_run)
