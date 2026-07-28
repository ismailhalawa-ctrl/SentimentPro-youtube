from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_WEAK_JWT_SECRETS = {
    "change-me",
    "changeme",
    "secret",
    "your-secret-key",
    "your-secret-key-here",
    "jwt-secret",
    "jwt_secret_key",
    "test",
    "testing",
    "development",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str
    db_pool_size: int = 20
    db_max_overflow: int = 30
    db_pool_recycle_seconds: int = 1800
    db_pool_timeout_seconds: int = 30

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 10_080
    cors_origins: str = "http://localhost:3000"
    environment: str = "development"
    youtube_api_key: str = ""

    frontend_url: str = "http://localhost:3000"

    backend_url: str = "http://localhost:8000"

    google_client_id: str = ""
    google_client_secret: str = ""

    sentiment_model_name: str = "Ammar-alhaj-ali/arabic-MARBERT-sentiment"
    sentiment_model_name_en: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    sentiment_model_name_multilingual: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    model_device: str = "cpu"
    torch_num_threads: int = 0

    fast_mode_batch_size: int = 128
    fast_mode_max_length: int = 128
    fast_mode_concurrent_batches: int = 8

    use_onnx_runtime: bool = True
    onnx_model_cache_dir: str = "./onnx_models"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"

    hybrid_escalation_confidence_threshold: float = 0.65
    hybrid_escalate_on_sarcasm: bool = True
    hybrid_escalate_on_mixed_language: bool = True
    hybrid_escalate_on_heavy_emoji: bool = True
    hybrid_decision_policy: str = "highest_confidence"

    llm_batch_classification_size: int = 400

    llm_max_concurrent_batches: int = 15

    smart_mode_sample_size: int = 400
    hybrid_llm_sample_size: int = 400
    llm_sample_min_per_stratum: int = 5

    embedding_provider: str = "local-minilm-multilingual"
    local_embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
    openai_embedding_model: str = "text-embedding-3-small"

    vector_db_provider: str = "chroma"
    vector_db_persist_dir: str = "./chroma_data"
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    pinecone_index_name: str = "youtube-comments"

    rag_top_k: int = 40

    audience_assistant_max_tool_calls: int = 6
    audience_assistant_history_limit: int = 20

    ai_daily_request_limit: int = 200
    ai_daily_token_limit: int = 300_000
    ai_monthly_request_limit: int = 3_000
    ai_monthly_token_limit: int = 5_000_000

    ai_daily_request_limit_pro: int = 1_000
    ai_daily_token_limit_pro: int = 1_500_000
    ai_monthly_request_limit_pro: int = 15_000
    ai_monthly_token_limit_pro: int = 25_000_000

    redis_url: str = ""

    sentry_dsn: str = ""

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_use_tls: bool = True

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_id_pro: str = ""

    support_email: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.strip().lower() == "production"

    @model_validator(mode="after")
    def _validate_jwt_secret_strength(self) -> "Settings":
        if self.is_production:
            if len(self.jwt_secret_key) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY must be at least 32 characters in production. "
                    "Generate one with: openssl rand -hex 32"
                )
            if self.jwt_secret_key.strip().lower() in _WEAK_JWT_SECRETS:
                raise ValueError(
                    "JWT_SECRET_KEY is set to a known placeholder value. "
                    "Generate a real secret with: openssl rand -hex 32"
                )
        return self

    @property
    def cors_lan_origin_regex(self) -> str:
        return (
            r"^https?://("
            r"localhost"
            r"|127\.0\.0\.1"
            r"|192\.168\.\d{1,3}\.\d{1,3}"
            r"|10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            r"|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
            r")(:\d+)?$"
        )


settings = Settings()
