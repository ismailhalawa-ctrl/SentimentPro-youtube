import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from app import models as _models
from app.ai.providers.model_loader import is_sentiment_model_loaded, load_sentiment_model
from app.ai.providers.provider_registry import get_registered_provider_ids
from app.api.v1.ai_insights import router as ai_insights_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.audience_assistant import router as audience_assistant_router
from app.api.v1.auth import router as auth_router
from app.api.v1.billing import router as billing_router
from app.api.v1.support import router as support_router
from app.api.v1.users import router as users_router
from app.api.v1.youtube import router as youtube_router
from app.core.config import settings
from app.core.limiter import limiter
from app.core.logging_config import configure_logging
from app.core.request_id import RequestIdMiddleware
from app.core.security_headers import SecurityHeadersMiddleware
from app.database.session import SessionLocal

configure_logging(json_logs=settings.is_production)

logger = logging.getLogger(__name__)

if settings.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.environment, traces_sample_rate=0.1)
    logger.info("Sentry error monitoring initialized.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    import torch

    torch_threads = settings.torch_num_threads or os.cpu_count() or 1
    torch.set_num_threads(torch_threads)
    logger.info("PyTorch CPU inference threads set to %d", torch_threads)

    load_sentiment_model("sentiment_ar", settings.sentiment_model_name, settings.model_device)
    load_sentiment_model("sentiment_en", settings.sentiment_model_name_en, settings.model_device)
    load_sentiment_model(
        "sentiment_multilingual", settings.sentiment_model_name_multilingual, settings.model_device
    )
    logger.info("AI providers registered: %s", get_registered_provider_ids())
    yield


app = FastAPI(title="YouTube Comment Sentiment Analyzer PRO API", lifespan=lifespan)

app.state.limiter = limiter


def _handle_rate_limit_exceeded(request: Request, exc: Exception) -> Response:
    assert isinstance(exc, RateLimitExceeded)
    return _rate_limit_exceeded_handler(request, exc)


app.add_exception_handler(RateLimitExceeded, _handle_rate_limit_exceeded)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on our end. Please try again in a moment."},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=settings.cors_lan_origin_regex if not settings.is_production else None,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIdMiddleware)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(youtube_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(ai_insights_router, prefix="/api/v1")
app.include_router(audience_assistant_router, prefix="/api/v1")
app.include_router(billing_router, prefix="/api/v1")
app.include_router(support_router, prefix="/api/v1")


@app.get("/health")
def health():
    checks = {}

    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            checks["database"] = "ok"
        finally:
            db.close()
    except Exception:
        logger.exception("Health check: database connectivity failed")
        checks["database"] = "unavailable"

    models_loaded = all(
        is_sentiment_model_loaded(key) for key in ("sentiment_ar", "sentiment_en", "sentiment_multilingual")
    )
    checks["models"] = "ok" if models_loaded else "not_loaded"

    healthy = all(value == "ok" for value in checks.values())
    status_code = 200 if healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "ok" if healthy else "degraded", "checks": checks},
    )
