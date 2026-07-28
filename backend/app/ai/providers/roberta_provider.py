from app.ai.providers.provider_registry import register_provider
from app.ai.providers.transformer_sentiment_provider import TransformerSentimentProvider


@register_provider("roberta")
class RobertaProvider(TransformerSentimentProvider):
    provider_id = "roberta"
    languages = ("en",)
    model_key = "sentiment_en"
