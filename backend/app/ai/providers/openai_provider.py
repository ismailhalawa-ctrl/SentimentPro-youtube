import asyncio
import json
import logging
import time
from collections.abc import Callable
from typing import cast

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.errors import ProviderCallError, ProviderNotConfiguredError
from app.ai.interfaces.provider import AIProvider
from app.ai.interfaces.result import AnalysisResult
from app.ai.prompts import (
    audience_analysis,
    audience_intelligence_narrative,
    batch_complaint,
    batch_sentiment,
    batch_suggestion,
    executive_summary,
    faq_generation,
    sentiment,
    topic_clustering,
)
from app.ai.prompts.audience_assistant import build_final_answer_instruction
from app.ai.providers._batch_comment_classifier import run_batch_classification_chunk
from app.ai.providers._loop_scoped import LoopScopedValue
from app.ai.providers._retry import call_with_retry_and_timeout, compute_batch_timeout
from app.ai.providers.provider_registry import register_provider
from app.core.config import settings

logger = logging.getLogger(__name__)

_PROMPT_BUILDERS = {
    Capability.SENTIMENT: sentiment.build_prompt,
    Capability.EXECUTIVE_SUMMARY: executive_summary.build_prompt,
    Capability.AUDIENCE_ANALYSIS: audience_analysis.build_prompt,
    Capability.FAQ_GENERATION: faq_generation.build_prompt,
    Capability.TOPIC_CLUSTERING: topic_clustering.build_prompt,
    Capability.AUDIENCE_INTELLIGENCE_SCORE: audience_intelligence_narrative.build_prompt,
}

_BATCH_PROMPT_BUILDERS: dict[Capability, Callable[..., list[dict]]] = {
    Capability.SENTIMENT: batch_sentiment.build_prompt,
    Capability.COMPLAINT_EXTRACTION: batch_complaint.build_prompt,
    Capability.SUGGESTION_EXTRACTION: batch_suggestion.build_prompt,
}


def _build_client():
    from openai import AsyncOpenAI

    return AsyncOpenAI(api_key=settings.openai_api_key)


_client = LoopScopedValue(_build_client)


def _get_client():
    if not settings.openai_api_key:
        raise ProviderNotConfiguredError(
            "OPENAI_API_KEY is not set — SMART-mode OpenAI features are disabled."
        )
    return _client.get()


class _BaseOpenAIProvider(AIProvider):
    mode = AnalysisMode.SMART
    languages = ("ar", "en", "mixed", "auto")

    def is_available(self) -> bool:
        return bool(settings.openai_api_key)

    async def run(self, text: str, **kwargs) -> AnalysisResult:
        client = _get_client()
        start = time.monotonic()
        messages = _PROMPT_BUILDERS[self.capability](text, **kwargs)

        try:
            response = await call_with_retry_and_timeout(
                lambda: client.chat.completions.create(
                    model=settings.openai_model,
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
            )
        except Exception as exc:
            raise ProviderCallError(f"OpenAI call failed for {self.provider_id}: {exc}") from exc

        raw_content = response.choices[0].message.content or "{}"
        try:
            parsed = json.loads(raw_content)
        except json.JSONDecodeError:
            logger.warning("OpenAI provider %s returned non-JSON content", self.provider_id)
            parsed = {}

        elapsed_ms = (time.monotonic() - start) * 1000
        label = parsed.get("label") or parsed.get("overall_sentiment_label")
        confidence = parsed.get("confidence")

        return AnalysisResult(
            capability=self.capability,
            provider_id=self.provider_id,
            mode=self.mode,
            label=label,
            confidence=confidence if isinstance(confidence, int | float) else None,
            processing_time_ms=elapsed_ms,
            data=parsed,
            raw_output={"content": raw_content},
        )

    async def run_batch(self, texts: list[str], **kwargs) -> list[AnalysisResult]:
        build_prompt = _BATCH_PROMPT_BUILDERS.get(self.capability)
        if build_prompt is None:
            return await super().run_batch(texts, **kwargs)

        kwargs.pop("capability", None)

        client = _get_client()

        def _make_call_llm(item_count: int):
            async def call_llm(messages: list[dict]) -> str:
                response = await call_with_retry_and_timeout(
                    lambda: client.chat.completions.create(
                        model=settings.openai_model,
                        messages=messages,
                        response_format={"type": "json_object"},
                        temperature=0.2,
                    ),
                    timeout=compute_batch_timeout(item_count),
                )
                return response.choices[0].message.content or "{}"

            return call_llm

        chunk_size = settings.llm_batch_classification_size
        chunks = [texts[i : i + chunk_size] for i in range(0, len(texts), chunk_size)]

        semaphore = asyncio.Semaphore(settings.llm_max_concurrent_batches)

        async def _run_chunk(chunk: list[str]) -> list[AnalysisResult]:
            async with semaphore:
                return await run_batch_classification_chunk(
                    chunk,
                    self.capability,
                    self.provider_id,
                    self.mode,
                    build_prompt,
                    _make_call_llm(len(chunk)),
                    **kwargs,
                )

        chunk_results = await asyncio.gather(*[_run_chunk(chunk) for chunk in chunks])
        return [result for chunk_result in chunk_results for result in chunk_result]


@register_provider("openai-gpt-sentiment")
class OpenAISentimentProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-sentiment"
    capability = Capability.SENTIMENT


@register_provider("openai-gpt-executive-summary")
class OpenAIExecutiveSummaryProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-executive-summary"
    capability = Capability.EXECUTIVE_SUMMARY


@register_provider("openai-gpt-audience-analysis")
class OpenAIAudienceAnalysisProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-audience-analysis"
    capability = Capability.AUDIENCE_ANALYSIS


@register_provider("openai-gpt-complaint-extraction")
class OpenAIComplaintExtractionProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-complaint-extraction"
    capability = Capability.COMPLAINT_EXTRACTION


@register_provider("openai-gpt-suggestion-extraction")
class OpenAISuggestionExtractionProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-suggestion-extraction"
    capability = Capability.SUGGESTION_EXTRACTION


@register_provider("openai-gpt-faq-generation")
class OpenAIFAQGenerationProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-faq-generation"
    capability = Capability.FAQ_GENERATION


@register_provider("openai-gpt-topic-clustering")
class OpenAITopicClusteringProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-topic-clustering"
    capability = Capability.TOPIC_CLUSTERING


@register_provider("openai-gpt-audience-intelligence")
class OpenAIAudienceIntelligenceProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-audience-intelligence"
    capability = Capability.AUDIENCE_INTELLIGENCE_SCORE


@register_provider("openai-gpt-audience-assistant")
class OpenAIAudienceAssistantProvider(_BaseOpenAIProvider):
    provider_id = "openai-gpt-audience-assistant"
    capability = Capability.AUDIENCE_ASSISTANT

    async def run(self, text: str, **kwargs) -> AnalysisResult:
        if not settings.openai_api_key:
            raise ProviderNotConfiguredError(
                "OPENAI_API_KEY is not set — the Universal Audience Assistant is disabled."
            )
        return AnalysisResult(
            capability=self.capability,
            provider_id=self.provider_id,
            mode=self.mode,
            label="not_implemented",
            confidence=None,
            data={
                "answer": "The Universal Audience Assistant's reasoning loop isn't implemented yet.",
                "citations": [],
            },
        )

    def build_conversation_state(self, system_prompt: str, history: list[dict], question: str) -> list[dict]:
        messages = [{"role": "system", "content": system_prompt}]
        for turn in history:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": question})
        return messages

    async def generate_step(
        self, state: object, force_final: bool = False, excluded_tools: set[str] | None = None
    ) -> dict:
        client = _get_client()

        messages = list(cast(list, state))
        if force_final:
            messages.append({"role": "system", "content": build_final_answer_instruction()})

        kwargs: dict[str, object] = {
            "model": settings.openai_model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }
        if not force_final:
            from app.ai.tools import get_tool_schemas

            kwargs["tools"] = get_tool_schemas("openai", exclude=excluded_tools)
            kwargs["tool_choice"] = "auto"

        try:
            response = await call_with_retry_and_timeout(lambda: client.chat.completions.create(**kwargs))
        except Exception as exc:
            raise ProviderCallError(f"OpenAI call failed for {self.provider_id}: {exc}") from exc

        if not response.choices:
            raise ProviderCallError(f"OpenAI returned no choices for {self.provider_id}.")

        usage = getattr(response, "usage", None)
        token_usage = {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) or 0,
            "completion_tokens": getattr(usage, "completion_tokens", 0) or 0,
        }

        message = response.choices[0].message
        if message.tool_calls:
            return {
                "content": None,
                "tool_calls": [
                    {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
                    for tc in message.tool_calls
                ],
                "_raw": message,
                "token_usage": token_usage,
            }
        return {"content": message.content, "tool_calls": [], "_raw": message, "token_usage": token_usage}

    def append_tool_round(
        self, state: object, tool_calls: list[dict], tool_results: list[dict], raw: object
    ) -> list[dict]:
        state = list(cast(list, state))
        state.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {"name": tc["name"], "arguments": tc["arguments"]},
                    }
                    for tc in tool_calls
                ],
            }
        )
        for result in tool_results:
            state.append({"role": "tool", "tool_call_id": result["id"], "content": result["content"]})
        return state
