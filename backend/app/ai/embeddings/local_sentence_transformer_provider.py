import asyncio

from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.core.config import settings

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(settings.local_embedding_model_name)
    return _model


class LocalSentenceTransformerProvider(EmbeddingProvider):
    provider_id = "local-minilm-multilingual"

    async def embed(self, texts: list[str]) -> list[list[float]]:
        def _run() -> list[list[float]]:
            model = _get_model()
            return model.encode(texts, convert_to_numpy=True).tolist()

        return await asyncio.to_thread(_run)
