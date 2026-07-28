from unittest.mock import patch


def test_register_rate_limit_triggers_429(client, unique_email):
    for i in range(5):
        response = client.post(
            "/api/v1/auth/register",
            json={"full_name": "Rate Test", "email": f"rl_{i}_{unique_email}", "password": "RateLimit123!"},
        )
        assert response.status_code == 201

    blocked = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Rate Test", "email": f"rl_overflow_{unique_email}", "password": "RateLimit123!"},
    )
    assert blocked.status_code == 429

    from app.database.session import SessionLocal
    from app.models.user import User

    session = SessionLocal()
    session.query(User).filter(User.email.like(f"rl_%_{unique_email}")).delete(synchronize_session=False)
    session.commit()
    session.close()


def test_login_rate_limit_triggers_429(client, registered_user):
    for _ in range(10):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": registered_user["email"], "password": "WrongPassword!"},
        )
        assert response.status_code == 401

    blocked = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": "WrongPassword!"},
    )
    assert blocked.status_code == 429


def test_job_creation_rate_limit_triggers_429(authenticated_client, db_session):
    from app.models.analysis_job import AnalysisJob

    created_job_ids = []
    with patch("app.api.v1.analysis.run_analysis_job"):
        for _ in range(5):
            response = authenticated_client.post(
                "/api/v1/analysis/jobs",
                json={
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "mode": "fast",
                    "max_comments": 25,
                },
            )
            assert response.status_code == 202
            created_job_ids.append(response.json()["id"])

        blocked = authenticated_client.post(
            "/api/v1/analysis/jobs",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "mode": "fast", "max_comments": 25},
        )
    assert blocked.status_code == 429

    db_session.query(AnalysisJob).filter(AnalysisJob.id.in_(created_job_ids)).delete(
        synchronize_session=False
    )
    db_session.commit()


def test_rate_limit_response_has_no_side_effects_on_state(client, unique_email):
    for i in range(5):
        client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Idempotent",
                "email": f"idem_{i}_{unique_email}",
                "password": "RateLimit123!",
            },
        )

    blocked = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Idempotent",
            "email": f"idem_overflow_{unique_email}",
            "password": "RateLimit123!",
        },
    )
    assert blocked.status_code == 429

    from app.database.session import SessionLocal
    from app.models.user import User

    session = SessionLocal()
    overflow_exists = (
        session.query(User).filter(User.email == f"idem_overflow_{unique_email}").first() is not None
    )
    session.query(User).filter(User.email.like(f"idem_%_{unique_email}")).delete(synchronize_session=False)
    session.commit()
    session.close()

    assert not overflow_exists
