import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

errors: list[str] = []


def check_required_settings_are_documented() -> None:
    sys.path.insert(0, str(BACKEND))
    from app.core.config import Settings

    required_fields = {
        name for name, field in Settings.model_fields.items() if field.is_required()
    }
    env_example = (BACKEND / ".env.example").read_text(encoding="utf-8")
    documented = set(re.findall(r"^([A-Z_][A-Z0-9_]*)=", env_example, re.MULTILINE))

    for field_name in required_fields:
        env_name = field_name.upper()
        if env_name not in documented:
            errors.append(
                f"Settings.{field_name} is required but {env_name} is not documented in "
                "backend/.env.example"
            )


def check_dockerfiles_have_healthcheck() -> None:
    for dockerfile in (BACKEND / "Dockerfile", FRONTEND / "Dockerfile"):
        content = dockerfile.read_text(encoding="utf-8")
        if "HEALTHCHECK" not in content:
            errors.append(f"{dockerfile.relative_to(ROOT)} has no HEALTHCHECK directive")


def check_backend_dependencies_are_pinned() -> None:
    requirements = BACKEND / "requirements.txt"
    for line in requirements.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-r "):
            continue
        if "==" not in line:
            errors.append(f"backend/requirements.txt has an unpinned dependency: {line}")


def check_alembic_baseline_creates_referenced_tables() -> None:
    versions_dir = BACKEND / "alembic" / "versions"
    created_tables: set[str] = set()
    referenced_tables: set[str] = set()

    for path in versions_dir.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        created_tables.update(re.findall(r"op\.create_table\(\s*'([a-zA-Z0-9_]+)'", text))
        referenced_tables.update(re.findall(r"ForeignKeyConstraint\(\[[^]]*\],\s*\['([a-zA-Z0-9_]+)\.", text))
        referenced_tables.update(re.findall(r"sa\.ForeignKey\('([a-zA-Z0-9_]+)\.", text))

    missing = referenced_tables - created_tables
    if missing:
        errors.append(
            "Alembic migrations reference tables that no migration ever creates "
            f"(a fresh database cannot be provisioned): {sorted(missing)}"
        )


def main() -> int:
    check_required_settings_are_documented()
    check_dockerfiles_have_healthcheck()
    check_backend_dependencies_are_pinned()
    check_alembic_baseline_creates_referenced_tables()

    if errors:
        print("Production readiness verification FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Production readiness verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
