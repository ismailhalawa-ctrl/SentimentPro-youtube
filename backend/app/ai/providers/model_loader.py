import logging
import time

from app.core.config import settings

logger = logging.getLogger(__name__)

_models: dict[str, tuple[object, object, dict[int, str]]] = {}


def load_sentiment_model(key: str, model_name: str, device: str) -> None:
    from transformers import AutoTokenizer

    start = time.monotonic()
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if settings.use_onnx_runtime:
        logger.info("Loading sentiment model [%s] %s via ONNX Runtime (INT8 quantized)...", key, model_name)
        model = _load_quantized_onnx_model(key, model_name)
    else:
        logger.info("Loading sentiment model [%s] %s on %s...", key, model_name, device)
        from transformers import AutoModelForSequenceClassification

        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.to(device)
        model.eval()

    id2label = {i: label.lower() for i, label in model.config.id2label.items()}

    _models[key] = (tokenizer, model, id2label)

    elapsed = time.monotonic() - start
    logger.info("Sentiment model [%s] loaded in %.2fs. Labels: %s", key, elapsed, id2label)


def _onnx_session_options():
    # default intra_op_num_threads is the full core count per session, but
    # FAST mode runs concurrent_batches sessions at once (see
    # INFERENCE_EXECUTOR in transformer_sentiment_provider.py), so they all
    # fight over every core. cap threads per session so concurrency actually
    # parallelizes instead of oversubscribing.
    import os

    from onnxruntime import SessionOptions

    cpu_count = os.cpu_count() or 1
    intra_op_threads = max(1, cpu_count // max(1, settings.fast_mode_concurrent_batches))

    options = SessionOptions()
    options.intra_op_num_threads = intra_op_threads
    options.inter_op_num_threads = 1
    return options


def _load_quantized_onnx_model(key: str, model_name: str):
    import os

    try:
        from optimum.onnxruntime import ORTModelForSequenceClassification, ORTQuantizer
        from optimum.onnxruntime.configuration import AutoQuantizationConfig
    except ImportError as exc:
        raise ImportError(
            "USE_ONNX_RUNTIME is true but the 'optimum' package isn't installed. "
            "Install it with: pip install -r requirements-onnx-optional.txt"
        ) from exc

    cache_dir = os.path.join(settings.onnx_model_cache_dir, key)
    quantized_file = os.path.join(cache_dir, "model_quantized.onnx")

    if not os.path.exists(quantized_file):
        logger.info(
            "No cached quantized ONNX model for [%s] yet — exporting and quantizing "
            "(one-time, subsequent startups load the cache directly)...",
            key,
        )
        export_dir = os.path.join(cache_dir, "_export")
        ort_model = ORTModelForSequenceClassification.from_pretrained(model_name, export=True)
        ort_model.save_pretrained(export_dir)

        quantizer = ORTQuantizer.from_pretrained(export_dir)
        qconfig = AutoQuantizationConfig.avx2(is_static=False, per_channel=False)
        quantizer.quantize(save_dir=cache_dir, quantization_config=qconfig)

    return ORTModelForSequenceClassification.from_pretrained(
        cache_dir, file_name="model_quantized.onnx", session_options=_onnx_session_options()
    )


def get_sentiment_model(key: str):
    if key not in _models:
        raise RuntimeError(
            f"Sentiment model [{key}] was not loaded. load_sentiment_model() "
            "must be called during app startup (see main.py lifespan) before "
            "any request reaches that language's sentiment provider."
        )
    return _models[key]


def is_sentiment_model_loaded(key: str) -> bool:
    return key in _models
