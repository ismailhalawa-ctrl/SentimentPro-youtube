import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.limiter import limiter
from app.database.session import SessionLocal
from app.main import app
from app.models.user import User

TEST_PASSWORD = "IntegrationTest123!"


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    limiter.reset()
    yield
    limiter.reset()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def _clear_client_cookies(client):
    client.cookies.clear()
    yield
    client.cookies.clear()


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def unique_email():
    return f"pytest_{uuid.uuid4().hex[:16]}@example.com"


@pytest.fixture
def registered_user(client, db_session, unique_email):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Pytest Integration User", "email": unique_email, "password": TEST_PASSWORD},
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    yield {"id": user_id, "email": unique_email, "password": TEST_PASSWORD}

    db_session.query(User).filter(User.id == user_id).delete()
    db_session.commit()


@pytest.fixture
def authenticated_client(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    return client
