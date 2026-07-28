from app.ai.providers.provider_registry import register_provider
from app.ai.providers.transformer_sentiment_provider import TransformerSentimentProvider


@register_provider("xlmr-multilingual")
class MultilingualSentimentProvider(TransformerSentimentProvider):
    provider_id = "xlmr-multilingual"
    languages = ("mixed",)
    model_key = "sentiment_multilingual"
