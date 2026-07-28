import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import make_url

from alembic import context

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.database.base import Base
from app.models import (
    analysis_job,
    assistant,
    chat,
    comment_analysis,
    comment_analysis_result,
    embedding_index,
    job_insight,
    user,
)

config = context.config

_escaped_url = settings.database_url.replace("%", "%%")
config.set_main_option("sqlalchemy.url", _escaped_url)

_resolved = make_url(settings.database_url)
print(
    f"[alembic env.py] resolved connection -> "
    f"host={_resolved.host} port={_resolved.port} database={_resolved.database} "
    f"username={_resolved.username}"
)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
