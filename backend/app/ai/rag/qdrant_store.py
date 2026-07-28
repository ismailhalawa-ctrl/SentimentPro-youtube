import asyncio
import importlib.util
import uuid

from app.ai.rag.vector_store import VectorMatch, VectorStore
from app.core.config import settings

_client = None


def _try_import_qdrant() -> bool:
    return importlib.util.find_spec("qdrant_client") is not None


def _qdrant_point_id(original_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, original_id))


class QdrantStore(VectorStore):
    provider_id = "qdrant"

    def is_configured(self) -> bool:
        return bool(settings.qdrant_url) and _try_import_qdrant()

    def _get_client(self):
        global _client
        if _client is None:
            from qdrant_client import QdrantClient

            _client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        return _client

    async def upsert(
        self,
        collection_name: str,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        def _run() -> None:
            from qdrant_client.models import Distance, PointStruct, VectorParams

            client = self._get_client()
            if not client.collection_exists(collection_name):
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE),
                )
            points = [
                PointStruct(
                    id=_qdrant_point_id(ids[i]),
                    vector=embeddings[i],
                    payload={**metadatas[i], "document": documents[i], "_original_id": ids[i]},
                )
                for i in range(len(ids))
            ]
            client.upsert(collection_name=collection_name, points=points)

        await asyncio.to_thread(_run)

    async def delete_collection(self, collection_name: str) -> None:
        def _run() -> None:
            client = self._get_client()
            if client.collection_exists(collection_name):
                client.delete_collection(collection_name)

        await asyncio.to_thread(_run)

    async def query(
        self, collection_name: str, query_embedding: list[float], top_k: int
    ) -> list[VectorMatch]:
        def _run() -> list[VectorMatch]:
            client = self._get_client()
            if not client.collection_exists(collection_name):
                return []
            results = client.search(
                collection_name=collection_name, query_vector=query_embedding, limit=top_k
            )
            matches = []
            for r in results:
                payload = dict(r.payload or {})
                document = payload.pop("document", "")
                original_id = payload.pop("_original_id", str(r.id))
                matches.append(
                    VectorMatch(id=original_id, document=document, metadata=payload, score=r.score)
                )
            return matches

        return await asyncio.to_thread(_run)
