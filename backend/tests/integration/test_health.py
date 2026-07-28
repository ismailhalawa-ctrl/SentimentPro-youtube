from unittest.mock import patch


def test_health_reports_healthy_when_db_and_models_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["checks"]["database"] == "ok"
    assert body["checks"]["models"] == "ok"


def test_health_reports_degraded_when_database_unreachable(client):
    with patch("app.main.SessionLocal", side_effect=Exception("simulated database outage")):
        response = client.get("/health")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["checks"]["database"] == "unavailable"


def test_health_reports_degraded_when_model_not_loaded(client):
    with patch("app.main.is_sentiment_model_loaded", return_value=False):
        response = client.get("/health")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["checks"]["models"] == "not_loaded"


def test_health_response_has_no_sensitive_data(client):
    response = client.get("/health")
    body = response.json()
    serialized = str(body).lower()
    for forbidden in ("password", "secret", "token", "api_key"):
        assert forbidden not in serialized
