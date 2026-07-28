from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class VectorMatch:
    id: str
    document: str
    metadata: dict
    score: float


class VectorStore(ABC):
    provider_id: str

    def is_configured(self) -> bool:
        return True

    @abstractmethod
    async def upsert(
        self,
        collection_name: str,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def query(
        self, collection_name: str, query_embedding: list[float], top_k: int
    ) -> list[VectorMatch]:
        raise NotImplementedError

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None:
        raise NotImplementedError
