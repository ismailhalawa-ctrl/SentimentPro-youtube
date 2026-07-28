def test_security_headers_present_on_api_response(client):
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "camera=()" in response.headers["permissions-policy"]


def test_content_security_policy_present_on_api_response(client):
    response = client.get("/health")
    assert response.headers["content-security-policy"] == "default-src 'none'; frame-ancestors 'none'"


def test_content_security_policy_absent_on_docs(client):
    response = client.get("/docs")
    assert "content-security-policy" not in response.headers


def test_no_hsts_header_outside_production(client):
    response = client.get("/health")
    assert "strict-transport-security" not in response.headers


def test_request_id_header_present_and_echoed(client):
    response = client.get("/health", headers={"X-Request-ID": "test-request-id-123"})
    assert response.headers["x-request-id"] == "test-request-id-123"


def test_request_id_generated_when_absent(client):
    response = client.get("/health")
    assert response.headers["x-request-id"]
    assert len(response.headers["x-request-id"]) > 0


def test_cors_headers_allow_configured_origin(client):
    response = client.options(
        "/api/v1/auth/me",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_headers_reject_untrusted_origin(client):
    response = client.options(
        "/api/v1/auth/me",
        headers={
            "Origin": "https://evil-site.example",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") != "https://evil-site.example"
