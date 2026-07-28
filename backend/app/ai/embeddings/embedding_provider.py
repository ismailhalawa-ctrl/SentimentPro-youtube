from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    provider_id: str

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def is_available(self) -> bool:
        return True
