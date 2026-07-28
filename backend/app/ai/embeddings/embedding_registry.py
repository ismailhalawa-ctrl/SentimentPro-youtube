from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.core.config import settings

_instances: dict[str, EmbeddingProvider] = {}


def get_embedding_provider() -> EmbeddingProvider:
    provider_id = settings.embedding_provider
    if provider_id not in _instances:
        _instances[provider_id] = _build(provider_id)
    return _instances[provider_id]


def get_embedding_provider_by_id(provider_id: str) -> EmbeddingProvider:
    if provider_id not in _instances:
        _instances[provider_id] = _build(provider_id)
    return _instances[provider_id]


def _build(provider_id: str) -> EmbeddingProvider:
    if provider_id == "openai-embedding":
        from app.ai.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider

        return OpenAIEmbeddingProvider()
    from app.ai.embeddings.local_sentence_transformer_provider import (
        LocalSentenceTransformerProvider,
    )

    return LocalSentenceTransformerProvider()
