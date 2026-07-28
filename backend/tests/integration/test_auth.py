from unittest.mock import patch

from tests.integration.conftest import TEST_PASSWORD


def test_register_creates_user(client, db_session, unique_email):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "New User", "email": unique_email, "password": TEST_PASSWORD},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == unique_email
    assert body["full_name"] == "New User"
    assert "hashed_password" not in body
    assert "password" not in body

    from app.models.user import User

    db_session.query(User).filter(User.id == body["id"]).delete()
    db_session.commit()


def test_register_rejects_duplicate_email(client, registered_user):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Duplicate", "email": registered_user["email"], "password": TEST_PASSWORD},
    )
    assert response.status_code == 400


def test_register_rejects_short_password(client, unique_email):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Short Pw", "email": unique_email, "password": "short"},
    )
    assert response.status_code == 422


def test_register_rejects_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Bad Email", "email": "not-an-email", "password": TEST_PASSWORD},
    )
    assert response.status_code == 422


def test_register_rejects_blank_full_name(client, unique_email):
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "   ", "email": unique_email, "password": TEST_PASSWORD},
    )
    assert response.status_code == 422


def test_login_succeeds_with_correct_credentials(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies


def test_login_sets_httponly_secure_cookie_flags(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]},
    )
    set_cookie = response.headers.get("set-cookie", "")
    assert "httponly" in set_cookie.lower()
    assert "samesite=lax" in set_cookie.lower()


def test_login_rejects_wrong_password(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": "WrongPassword123!"},
    )
    assert response.status_code == 401
    assert "access_token" not in response.cookies


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody-at-all@example.com", "password": TEST_PASSWORD},
    )
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user_when_authenticated(authenticated_client, registered_user):
    response = authenticated_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == registered_user["email"]


def test_me_rejects_tampered_cookie(client):
    client.cookies.set("access_token", "not-a-real-jwt")
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_logout_clears_cookie(authenticated_client):
    response = authenticated_client.post("/api/v1/auth/logout")
    assert response.status_code == 204
    set_cookie = response.headers.get("set-cookie", "")
    assert "access_token=" in set_cookie

    me_response = authenticated_client.get("/api/v1/auth/me")
    assert me_response.status_code == 401


def test_forgot_password_does_not_leak_account_existence(client, registered_user):
    with patch("app.api.v1.auth.send_password_reset_email") as mock_send:
        known = client.post("/api/v1/auth/forgot-password", json={"email": registered_user["email"]})
        unknown = client.post("/api/v1/auth/forgot-password", json={"email": "ghost@example.com"})
    assert known.status_code == 200
    assert unknown.status_code == 200
    assert known.json()["message"] == unknown.json()["message"]
    mock_send.assert_called_once()


def test_forgot_password_sends_email_for_known_account(client, registered_user):
    with patch("app.api.v1.auth.send_password_reset_email") as mock_send:
        client.post("/api/v1/auth/forgot-password", json={"email": registered_user["email"]})
    mock_send.assert_called_once()
    call_args = mock_send.call_args[0]
    assert call_args[0] == registered_user["email"]
    assert "reset-password?token=" in call_args[1]


def test_reset_password_rejects_invalid_token(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": "not-a-real-token", "new_password": "BrandNewPassword123!"},
    )
    assert response.status_code == 400


def test_reset_password_rejects_short_password(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": "irrelevant", "new_password": "short"},
    )
    assert response.status_code == 422


def test_google_login_without_config_redirects_with_error(client):
    response = client.get("/api/v1/auth/google/login", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert "error=" in response.headers["location"] or "google" in response.headers["location"].lower()


def test_google_callback_rejects_state_mismatch(client):
    response = client.get(
        "/api/v1/auth/google/callback",
        params={"code": "fake-code", "state": "mismatched-state"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 307)
    assert "error=" in response.headers["location"]
