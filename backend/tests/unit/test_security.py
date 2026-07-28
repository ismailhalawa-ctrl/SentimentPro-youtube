from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_secure_token,
    hash_password,
    hash_token,
    verify_password,
)


def test_password_hash_roundtrip():
    hashed = hash_password("CorrectHorseBattery1!")
    assert hashed != "CorrectHorseBattery1!"
    assert verify_password("CorrectHorseBattery1!", hashed)


def test_password_hash_rejects_wrong_password():
    hashed = hash_password("CorrectHorseBattery1!")
    assert not verify_password("WrongPassword1!", hashed)


def test_password_hash_is_salted():
    first = hash_password("SamePassword1!")
    second = hash_password("SamePassword1!")
    assert first != second


def test_access_token_roundtrip():
    token = create_access_token("42")
    assert decode_access_token(token) == "42"


def test_access_token_rejects_tampering():
    token = create_access_token("42")
    tampered = token[:-4] + ("A" if token[-4] != "A" else "B") + token[-3:]
    assert decode_access_token(tampered) is None


def test_access_token_rejects_wrong_secret():
    payload = {
        "sub": "42",
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, "a-completely-different-secret-key-value", algorithm=settings.jwt_algorithm)
    assert decode_access_token(token) is None


def test_access_token_rejects_expired():
    payload = {
        "sub": "42",
        "exp": datetime.now(UTC) - timedelta(minutes=1),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    assert decode_access_token(token) is None


def test_access_token_rejects_none_algorithm():
    payload = {
        "sub": "42",
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    forged = jwt.encode(payload, "", algorithm="none")
    assert decode_access_token(forged) is None


def test_access_token_rejects_missing_subject():
    payload = {"exp": datetime.now(UTC) + timedelta(minutes=5)}
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    assert decode_access_token(token) is None


def test_generate_secure_token_is_unique_and_url_safe():
    tokens = {generate_secure_token() for _ in range(20)}
    assert len(tokens) == 20
    for token in tokens:
        assert all(c.isalnum() or c in "-_" for c in token)


def test_hash_token_is_deterministic():
    raw = generate_secure_token()
    assert hash_token(raw) == hash_token(raw)


def test_hash_token_differs_per_input():
    assert hash_token("token-a") != hash_token("token-b")


@pytest.mark.parametrize("algorithm", ["HS512", "HS384"])
def test_access_token_rejects_different_algorithm(algorithm):
    payload = {
        "sub": "42",
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=algorithm)
    assert decode_access_token(token) is None
