import asyncio
import json
import logging
import time
from collections.abc import Callable
from typing import Any, cast

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


def _configure() -> None:
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)


_configuration = LoopScopedValue(_configure)


def _ensure_configured():
    if not settings.gemini_api_key:
        raise ProviderNotConfiguredError(
            "GEMINI_API_KEY is not set — SMART-mode Gemini features are disabled."
        )
    _configuration.get()


class _BaseGeminiProvider(AIProvider):
    mode = AnalysisMode.SMART
    languages = ("ar", "en", "mixed", "auto")

    def is_available(self) -> bool:
        return bool(settings.gemini_api_key)

    async def run(self, text: str, **kwargs) -> AnalysisResult:
        _ensure_configured()
        start = time.monotonic()
        messages = _PROMPT_BUILDERS[self.capability](text, **kwargs)
        system_instruction = next((m["content"] for m in messages if m["role"] == "system"), None)
        contents = [
            {"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]}
            for m in messages
            if m["role"] != "system"
        ]

        try:
            import google.generativeai as genai

            model = genai.GenerativeModel(settings.gemini_model, system_instruction=system_instruction)
            response = await call_with_retry_and_timeout(
                lambda: model.generate_content_async(
                    contents,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json", temperature=0.2
                    ),
                )
            )
        except Exception as exc:
            raise ProviderCallError(f"Gemini call failed for {self.provider_id}: {exc}") from exc

        raw_content = response.text or "{}"
        try:
            parsed = json.loads(raw_content)
        except json.JSONDecodeError:
            logger.warning("Gemini provider %s returned non-JSON content", self.provider_id)
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

        _ensure_configured()

        def _make_call_llm(item_count: int):
            async def call_llm(messages: list[dict]) -> str:
                system_instruction = next((m["content"] for m in messages if m["role"] == "system"), None)
                user_content = "\n\n".join(m["content"] for m in messages if m["role"] != "system")
                import google.generativeai as genai

                model = genai.GenerativeModel(settings.gemini_model, system_instruction=system_instruction)
                response = await call_with_retry_and_timeout(
                    lambda: model.generate_content_async(
                        user_content,
                        generation_config=genai.GenerationConfig(
                            response_mime_type="application/json", temperature=0.2
                        ),
                    ),
                    timeout=compute_batch_timeout(item_count),
                )
                return response.text or "{}"

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


@register_provider("gemini-sentiment")
class GeminiSentimentProvider(_BaseGeminiProvider):
    provider_id = "gemini-sentiment"
    capability = Capability.SENTIMENT


@register_provider("gemini-executive-summary")
class GeminiExecutiveSummaryProvider(_BaseGeminiProvider):
    provider_id = "gemini-executive-summary"
    capability = Capability.EXECUTIVE_SUMMARY


@register_provider("gemini-audience-analysis")
class GeminiAudienceAnalysisProvider(_BaseGeminiProvider):
    provider_id = "gemini-audience-analysis"
    capability = Capability.AUDIENCE_ANALYSIS


@register_provider("gemini-complaint-extraction")
class GeminiComplaintExtractionProvider(_BaseGeminiProvider):
    provider_id = "gemini-complaint-extraction"
    capability = Capability.COMPLAINT_EXTRACTION


@register_provider("gemini-suggestion-extraction")
class GeminiSuggestionExtractionProvider(_BaseGeminiProvider):
    provider_id = "gemini-suggestion-extraction"
    capability = Capability.SUGGESTION_EXTRACTION


@register_provider("gemini-faq-generation")
class GeminiFAQGenerationProvider(_BaseGeminiProvider):
    provider_id = "gemini-faq-generation"
    capability = Capability.FAQ_GENERATION


@register_provider("gemini-topic-clustering")
class GeminiTopicClusteringProvider(_BaseGeminiProvider):
    provider_id = "gemini-topic-clustering"
    capability = Capability.TOPIC_CLUSTERING


@register_provider("gemini-audience-intelligence")
class GeminiAudienceIntelligenceProvider(_BaseGeminiProvider):
    provider_id = "gemini-audience-intelligence"
    capability = Capability.AUDIENCE_INTELLIGENCE_SCORE


@register_provider("gemini-audience-assistant")
class GeminiAudienceAssistantProvider(_BaseGeminiProvider):
    provider_id = "gemini-audience-assistant"
    capability = Capability.AUDIENCE_ASSISTANT

    async def run(self, text: str, **kwargs) -> AnalysisResult:
        if not settings.gemini_api_key:
            raise ProviderNotConfiguredError(
                "GEMINI_API_KEY is not set — the Universal Audience Assistant is disabled."
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

    def build_conversation_state(self, system_prompt: str, history: list[dict], question: str) -> dict:
        contents = [
            {"role": "model" if turn["role"] == "assistant" else "user", "parts": [turn["content"]]}
            for turn in history
        ]
        contents.append({"role": "user", "parts": [question]})
        return {"contents": contents, "system_prompt": system_prompt}

    async def generate_step(
        self, state: object, force_final: bool = False, excluded_tools: set[str] | None = None
    ) -> dict:
        _ensure_configured()
        import google.generativeai as genai

        state = cast(dict, state)
        system_instruction = state["system_prompt"]
        generation_config_kwargs: dict[str, object] = {"temperature": 0.2}
        tools = None

        if force_final:
            system_instruction = f"{system_instruction}\n\n{build_final_answer_instruction()}"
            generation_config_kwargs["response_mime_type"] = "application/json"
        else:
            from app.ai.tools import get_tool_schemas

            gemini_schemas = get_tool_schemas("gemini", exclude=excluded_tools)
            tools = [
                genai.protos.Tool(
                    function_declarations=[
                        genai.protos.FunctionDeclaration(
                            name=s["name"], description=s["description"], parameters=s["parameters"]
                        )
                        for s in gemini_schemas
                    ]
                )
            ]

        model = genai.GenerativeModel(
            settings.gemini_model, system_instruction=system_instruction, tools=tools
        )

        try:
            response = await call_with_retry_and_timeout(
                lambda: model.generate_content_async(
                    state["contents"], generation_config=genai.GenerationConfig(**generation_config_kwargs)
                )
            )
        except Exception as exc:
            raise ProviderCallError(f"Gemini call failed for {self.provider_id}: {exc}") from exc

        if not response.candidates:
            raise ProviderCallError(f"Gemini returned no candidates for {self.provider_id}.")

        usage_metadata = getattr(response, "usage_metadata", None)
        token_usage = {
            "prompt_tokens": getattr(usage_metadata, "prompt_token_count", 0) or 0,
            "completion_tokens": getattr(usage_metadata, "candidates_token_count", 0) or 0,
        }

        candidate = response.candidates[0]
        function_calls = [part.function_call for part in candidate.content.parts if part.function_call.name]

        if function_calls:
            return {
                "content": None,
                "tool_calls": [
                    {"id": f"gemini_call_{i}", "name": fc.name, "arguments": json.dumps(dict(fc.args))}
                    for i, fc in enumerate(function_calls)
                ],
                "_raw": candidate.content,
                "token_usage": token_usage,
            }

        text = "".join(part.text for part in candidate.content.parts if part.text)
        return {"content": text, "tool_calls": [], "_raw": candidate.content, "token_usage": token_usage}

    def append_tool_round(
        self, state: object, tool_calls: list[dict], tool_results: list[dict], raw: object
    ) -> dict:
        import google.generativeai as genai

        state = cast(dict, state)
        raw_content = cast(Any, raw)
        contents = list(state["contents"])
        contents.append({"role": "model", "parts": raw_content.parts})
        contents.append(
            {
                "role": "user",
                "parts": [
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=result["name"], response={"result": json.loads(result["content"])}
                        )
                    )
                    for result in tool_results
                ],
            }
        )
        return {"contents": contents, "system_prompt": state["system_prompt"]}
