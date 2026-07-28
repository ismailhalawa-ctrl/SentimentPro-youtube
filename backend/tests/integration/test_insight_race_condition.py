from unittest.mock import AsyncMock, patch

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.result import AnalysisResult
from app.models.ai_usage import AIUsageLog
from app.models.analysis_job import AnalysisJob
from app.models.job_insight import JobInsight
from app.services.insight_service import get_or_generate_insight


def test_job_insight_unique_constraint_rejects_duplicate(db_session, registered_user):
    job = AnalysisJob(
        owner_id=registered_user["id"],
        video_url="https://www.youtube.com/watch?v=racecond11",
        video_id="racecond11",
        options_json={},
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    db_session.add(
        JobInsight(
            job_id=job.id,
            capability=Capability.EXECUTIVE_SUMMARY.value,
            provider_id="p",
            mode="smart",
            result_json={},
        )
    )
    db_session.commit()

    db_session.add(
        JobInsight(
            job_id=job.id,
            capability=Capability.EXECUTIVE_SUMMARY.value,
            provider_id="p",
            mode="smart",
            result_json={},
        )
    )
    from sqlalchemy.exc import IntegrityError

    try:
        db_session.commit()
        raised = False
    except IntegrityError:
        db_session.rollback()
        raised = True

    assert raised

    db_session.query(JobInsight).filter(JobInsight.job_id == job.id).delete()
    db_session.query(AnalysisJob).filter(AnalysisJob.id == job.id).delete()
    db_session.commit()


async def test_concurrent_generation_race_returns_existing_row_instead_of_crashing(
    db_session, registered_user
):
    job = AnalysisJob(
        owner_id=registered_user["id"],
        video_url="https://www.youtube.com/watch?v=racecond22",
        video_id="racecond22",
        options_json={},
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    fake_result = AnalysisResult(
        capability=Capability.EXECUTIVE_SUMMARY,
        provider_id="test-provider",
        mode=AnalysisMode.SMART,
        label="ok",
        confidence=1.0,
        data={"overview": "race test", "overall_sentiment_label": "mixed"},
    )

    def _insert_competing_row_then_call(*args, **kwargs):
        from app.database.session import SessionLocal

        competing_session = SessionLocal()
        competing_session.add(
            JobInsight(
                job_id=job.id,
                capability=Capability.EXECUTIVE_SUMMARY.value,
                provider_id="competing-writer",
                mode="smart",
                result_json={"overview": "the other writer won the race"},
            )
        )
        competing_session.commit()
        competing_session.close()
        return fake_result

    mock_chain = AsyncMock(side_effect=_insert_competing_row_then_call)

    with patch.dict("app.services.insight_service._CHAINS", {Capability.EXECUTIVE_SUMMARY: mock_chain}):
        result = await get_or_generate_insight(
            db_session, job, Capability.EXECUTIVE_SUMMARY, registered_user["id"]
        )

    assert result.status == "ok"
    assert result.data["overview"] == "the other writer won the race"

    rows = db_session.query(JobInsight).filter(JobInsight.job_id == job.id).all()
    assert len(rows) == 1

    db_session.query(JobInsight).filter(JobInsight.job_id == job.id).delete()
    db_session.query(AIUsageLog).filter(AIUsageLog.user_id == registered_user["id"]).delete()
    db_session.query(AnalysisJob).filter(AnalysisJob.id == job.id).delete()
    db_session.commit()
