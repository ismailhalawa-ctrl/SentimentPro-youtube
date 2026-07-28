import pytest
from pydantic import ValidationError

from app.core.config import Settings

BASE_ENV = {
    "database_url": "mssql+pyodbc://user:pass@localhost:1433/db",
    "jwt_secret_key": "a-sufficiently-long-development-secret-key-value",
}


@pytest.mark.parametrize("value", ["production", "Production", "PRODUCTION", " production ", "PrOdUcTiOn"])
def test_is_production_case_and_whitespace_insensitive(value):
    settings = Settings(**BASE_ENV, environment=value)
    assert settings.is_production is True


@pytest.mark.parametrize("value", ["development", "staging", "test", ""])
def test_is_production_false_for_non_production_values(value):
    settings = Settings(**BASE_ENV, environment=value)
    assert settings.is_production is False


def test_weak_jwt_secret_rejected_in_production():
    with pytest.raises(ValidationError):
        Settings(
            database_url=BASE_ENV["database_url"],
            jwt_secret_key="change-me",
            environment="production",
        )


def test_short_jwt_secret_rejected_in_production():
    with pytest.raises(ValidationError):
        Settings(
            database_url=BASE_ENV["database_url"],
            jwt_secret_key="short",
            environment="production",
        )


def test_strong_jwt_secret_accepted_in_production():
    settings = Settings(
        database_url=BASE_ENV["database_url"],
        jwt_secret_key="a-genuinely-random-64-character-secret-key-value-for-prod-use",
        environment="production",
    )
    assert settings.is_production is True


def test_weak_jwt_secret_allowed_outside_production():
    settings = Settings(
        database_url=BASE_ENV["database_url"],
        jwt_secret_key="change-me",
        environment="development",
    )
    assert settings.jwt_secret_key == "change-me"


def test_cors_origins_list_parses_and_trims():
    settings = Settings(**BASE_ENV, cors_origins="http://a.com, http://b.com,http://c.com")
    assert settings.cors_origins_list == ["http://a.com", "http://b.com", "http://c.com"]


def test_cors_origins_list_empty_string_yields_empty_list():
    settings = Settings(**BASE_ENV, cors_origins="")
    assert settings.cors_origins_list == []


def test_cors_lan_origin_regex_matches_private_ranges():
    import re

    pattern = re.compile(Settings(**BASE_ENV).cors_lan_origin_regex)
    for origin in [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.19:3000",
        "http://10.0.0.5:3000",
        "http://172.16.0.1:3000",
    ]:
        assert pattern.match(origin), origin


def test_cors_lan_origin_regex_rejects_public_ip():
    import re

    pattern = re.compile(Settings(**BASE_ENV).cors_lan_origin_regex)
    assert not pattern.match("http://8.8.8.8:3000")
