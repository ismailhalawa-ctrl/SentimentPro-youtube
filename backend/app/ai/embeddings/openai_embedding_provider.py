from app.ai.embeddings.embedding_provider import EmbeddingProvider
from app.ai.interfaces.errors import ProviderNotConfiguredError
from app.ai.providers._loop_scoped import LoopScopedValue
from app.core.config import settings


def _build_client():
    from openai import AsyncOpenAI

    return AsyncOpenAI(api_key=settings.openai_api_key)


_client = LoopScopedValue(_build_client)


class OpenAIEmbeddingProvider(EmbeddingProvider):
    provider_id = "openai-embedding"

    def is_available(self) -> bool:
        return bool(settings.openai_api_key)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not settings.openai_api_key:
            raise ProviderNotConfiguredError(
                "OPENAI_API_KEY is not set — the openai-embedding provider is disabled."
            )
        client = _client.get()
        response = await client.embeddings.create(model=settings.openai_embedding_model, input=texts)
        return [item.embedding for item in response.data]
