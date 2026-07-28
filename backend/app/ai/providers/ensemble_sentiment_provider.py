import asyncio
import time

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.provider import AIProvider
from app.ai.interfaces.result import AnalysisResult
from app.ai.providers.ensemble_fusion import fuse_probability_distributions
from app.ai.providers.provider_registry import register_provider
from app.ai.providers.transformer_sentiment_provider import INFERENCE_EXECUTOR, run_model_probs

# down from 0.85/0.5: that sent ~60% of Arabic comments through the
# expensive second pass. tried 0.75/0.30 first but it regressed a formulaic
# religious phrase (primary model confidently wrong, second model right),
# 0.80/0.40 avoids that regression and still cuts second-pass calls ~17%.
_CONFIDENT_SCORE_THRESHOLD = 0.80
_CONFIDENT_MARGIN_THRESHOLD = 0.40


def _margin(probs: dict[str, float]) -> float:
    ranked = sorted(probs.values(), reverse=True)
    return ranked[0] - ranked[1] if len(ranked) >= 2 else 1.0


def _is_confident(probs: dict[str, float]) -> bool:
    return max(probs.values()) >= _CONFIDENT_SCORE_THRESHOLD and _margin(probs) >= _CONFIDENT_MARGIN_THRESHOLD


@register_provider("marbert-xlmr-ensemble")
class EnsembleSentimentProvider(AIProvider):
    provider_id = "marbert-xlmr-ensemble"
    capability = Capability.SENTIMENT
    mode = AnalysisMode.FAST
    languages = ("ar",)
    primary_model_key = "sentiment_ar"
    secondary_model_key = "sentiment_multilingual"

    async def run(self, text: str, **kwargs) -> AnalysisResult:
        results = await self.run_batch([text], **kwargs)
        return results[0]

    async def run_batch(self, texts: list[str], **kwargs) -> list[AnalysisResult]:
        loop = asyncio.get_running_loop()
        start = time.monotonic()

        primary_probs = await loop.run_in_executor(
            INFERENCE_EXECUTOR, run_model_probs, self.primary_model_key, texts
        )

        uncertain_indices = [i for i, probs in enumerate(primary_probs) if not _is_confident(probs)]

        secondary_probs: dict[int, dict[str, float]] = {}
        if uncertain_indices:
            uncertain_texts = [texts[i] for i in uncertain_indices]
            secondary_results = await loop.run_in_executor(
                INFERENCE_EXECUTOR, run_model_probs, self.secondary_model_key, uncertain_texts
            )
            secondary_probs = dict(zip(uncertain_indices, secondary_results, strict=True))

        elapsed_ms = (time.monotonic() - start) * 1000 / max(len(texts), 1)

        results = []
        for i in range(len(texts)):
            if i in secondary_probs:
                fused = fuse_probability_distributions([primary_probs[i], secondary_probs[i]])
                data = {
                    "all_probs": fused,
                    "ensemble_members": {
                        self.primary_model_key: primary_probs[i],
                        self.secondary_model_key: secondary_probs[i],
                    },
                    "ensemble_fused": True,
                }
            else:
                fused = primary_probs[i]
                data = {"all_probs": fused, "ensemble_fused": False}

            top_label = max(fused, key=lambda label: fused[label])
            results.append(
                AnalysisResult(
                    capability=self.capability,
                    provider_id=self.provider_id,
                    mode=self.mode,
                    label=top_label,
                    confidence=fused[top_label],
                    processing_time_ms=elapsed_ms,
                    data=data,
                )
            )
        return results
