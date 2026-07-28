from unittest.mock import AsyncMock, patch

import pytest

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.errors import ProviderNotConfiguredError
from app.ai.interfaces.result import AnalysisResult
from app.models.ai_usage import AIUsageLog
from app.models.analysis_job import AnalysisJob
from app.models.job_insight import JobInsight
from app.services.ai_usage_service import UsageLimitExceededError
from app.services.insight_service import get_or_generate_insight


@pytest.fixture
def analysis_job(db_session, registered_user):
    job = AnalysisJob(
        owner_id=registered_user["id"],
        video_url="https://www.youtube.com/watch?v=testvideo11",
        video_id="testvideo11",
        options_json={},
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    yield job
    db_session.query(JobInsight).filter(JobInsight.job_id == job.id).delete()
    db_session.query(AIUsageLog).filter(AIUsageLog.user_id == registered_user["id"]).delete()
    db_session.query(AnalysisJob).filter(AnalysisJob.id == job.id).delete()
    db_session.commit()


def _fake_result():
    return AnalysisResult(
        capability=Capability.EXECUTIVE_SUMMARY,
        provider_id="test-provider",
        mode=AnalysisMode.SMART,
        label="ok",
        confidence=1.0,
        data={"overview": "test overview", "overall_sentiment_label": "mixed"},
    )


def _patched_chain(mock_chain):
    return patch.dict("app.services.insight_service._CHAINS", {Capability.EXECUTIVE_SUMMARY: mock_chain})


async def test_generates_and_caches_insight(db_session, analysis_job, registered_user):
    mock_chain = AsyncMock(return_value=_fake_result())
    with _patched_chain(mock_chain):
        first = await get_or_generate_insight(
            db_session, analysis_job, Capability.EXECUTIVE_SUMMARY, registered_user["id"]
        )
        assert first.status == "ok"
        assert mock_chain.await_count == 1

        second = await get_or_generate_insight(
            db_session, analysis_job, Capability.EXECUTIVE_SUMMARY, registered_user["id"]
        )
        assert second.status == "ok"
        assert mock_chain.await_count == 1

    usage_rows = db_session.query(AIUsageLog).filter(AIUsageLog.user_id == registered_user["id"]).all()
    assert len(usage_rows) == 1


async def test_returns_rate_limited_when_quota_exceeded(db_session, analysis_job, registered_user):
    mock_chain = AsyncMock(return_value=_fake_result())
    with (
        patch(
            "app.services.insight_service.ai_usage_service.check_usage_limit",
            side_effect=UsageLimitExceededError("quota exceeded"),
        ),
        _patched_chain(mock_chain),
    ):
        result = await get_or_generate_insight(
            db_session, analysis_job, Capability.EXECUTIVE_SUMMARY, registered_user["id"]
        )
    assert result.status == "rate_limited"
    assert mock_chain.await_count == 0


async def test_returns_unavailable_when_provider_not_configured(db_session, analysis_job, registered_user):
    mock_chain = AsyncMock(side_effect=ProviderNotConfiguredError("no api key"))
    with _patched_chain(mock_chain):
        result = await get_or_generate_insight(
            db_session, analysis_job, Capability.EXECUTIVE_SUMMARY, registered_user["id"]
        )
    assert result.status == "unavailable"

    usage_rows = db_session.query(AIUsageLog).filter(AIUsageLog.user_id == registered_user["id"]).all()
    assert len(usage_rows) == 0


async def test_unknown_capability_returns_error(db_session, analysis_job, registered_user):
    result = await get_or_generate_insight(
        db_session, analysis_job, Capability.SENTIMENT, registered_user["id"]
    )
    assert result.status == "error"
