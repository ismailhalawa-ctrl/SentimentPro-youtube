import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.provider import AIProvider
from app.ai.interfaces.result import AnalysisResult
from app.ai.providers.model_loader import get_sentiment_model
from app.core.config import settings

INFERENCE_EXECUTOR = ThreadPoolExecutor(
    max_workers=settings.fast_mode_concurrent_batches, thread_name_prefix="fast-inference"
)


def run_model_probs(model_key: str, texts: list[str]) -> list[dict[str, float]]:
    import torch

    tokenizer, model, id2label = get_sentiment_model(model_key)

    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=settings.fast_mode_max_length,
        return_tensors="pt",
    )
    with torch.no_grad():
        outputs = model(**inputs)
        logits = torch.as_tensor(outputs.logits)
        probs = torch.nn.functional.softmax(logits, dim=-1)

    return [{id2label[i].lower(): float(row[i].item()) for i in range(len(row))} for row in probs]


class TransformerSentimentProvider(AIProvider):
    capability = Capability.SENTIMENT
    mode = AnalysisMode.FAST
    model_key: str

    async def run(self, text: str, **kwargs) -> AnalysisResult:
        results = await self.run_batch([text], **kwargs)
        return results[0]

    async def run_batch(self, texts: list[str], **kwargs) -> list[AnalysisResult]:
        def _run_inference() -> list[dict]:
            start = time.monotonic()
            all_probs_list = run_model_probs(self.model_key, texts)
            elapsed_ms = (time.monotonic() - start) * 1000 / max(len(texts), 1)

            batch_output = []
            for all_probs in all_probs_list:
                top_label = max(all_probs, key=lambda label: all_probs[label])
                batch_output.append(
                    {
                        "label": top_label,
                        "score": all_probs[top_label],
                        "processing_time_ms": elapsed_ms,
                        "all_probs": all_probs,
                    }
                )
            return batch_output

        loop = asyncio.get_running_loop()
        raw_results = await loop.run_in_executor(INFERENCE_EXECUTOR, _run_inference)

        return [
            AnalysisResult(
                capability=self.capability,
                provider_id=self.provider_id,
                mode=self.mode,
                label=r["label"],
                confidence=r["score"],
                processing_time_ms=r["processing_time_ms"],
                data={"all_probs": r["all_probs"]},
                raw_output=r,
            )
            for r in raw_results
        ]
