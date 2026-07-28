import pytest

from app.ai.providers.model_loader import is_sentiment_model_loaded, load_sentiment_model
from app.core.config import settings


@pytest.fixture(scope="session", autouse=True)
def _load_real_models():
    if not is_sentiment_model_loaded("sentiment_ar"):
        load_sentiment_model("sentiment_ar", settings.sentiment_model_name, settings.model_device)
    if not is_sentiment_model_loaded("sentiment_en"):
        load_sentiment_model("sentiment_en", settings.sentiment_model_name_en, settings.model_device)
    if not is_sentiment_model_loaded("sentiment_multilingual"):
        load_sentiment_model(
            "sentiment_multilingual", settings.sentiment_model_name_multilingual, settings.model_device
        )
    yield
