from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c8f3a1d7e5b9'
down_revision: Union[str, None] = 'b7e1f4a8c6d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_CASCADE_FKS = [
    ('analysis_jobs', 'owner_id', 'users', 'id'),
    ('comment_analyses', 'job_id', 'analysis_jobs', 'id'),
    ('comment_analysis_results', 'comment_id', 'comment_analyses', 'id'),
    ('job_insights', 'job_id', 'analysis_jobs', 'id'),
    ('embedding_indexes', 'job_id', 'analysis_jobs', 'id'),
    ('chat_sessions', 'job_id', 'analysis_jobs', 'id'),
    ('chat_messages', 'session_id', 'chat_sessions', 'id'),
    ('subscriptions', 'user_id', 'users', 'id'),
    ('ai_usage_logs', 'user_id', 'users', 'id'),
]

_SET_NULL_FKS = [
    ('support_messages', 'user_id', 'users', 'id'),
]

_FK_LOOKUP_SQL = sa.text(
    """
    SELECT fk.name
    FROM sys.foreign_keys fk
    JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
    JOIN sys.tables t ON t.object_id = fk.parent_object_id
    JOIN sys.columns c ON c.object_id = t.object_id AND c.column_id = fkc.parent_column_id
    WHERE t.name = :table_name AND c.name = :column_name
    """
)


def _existing_fk_name(connection, table, column):
    name = connection.execute(_FK_LOOKUP_SQL, {"table_name": table, "column_name": column}).scalar()
    if name is None:
        raise RuntimeError(f"No foreign key found on {table}.{column}")
    return name


def upgrade() -> None:
    connection = op.get_bind()

    for table, column, ref_table, ref_column in _CASCADE_FKS:
        name = _existing_fk_name(connection, table, column)
        op.drop_constraint(name, table, type_='foreignkey')
        op.create_foreign_key(name, table, ref_table, [column], [ref_column], ondelete='CASCADE')

    for table, column, ref_table, ref_column in _SET_NULL_FKS:
        name = _existing_fk_name(connection, table, column)
        op.drop_constraint(name, table, type_='foreignkey')
        op.create_foreign_key(name, table, ref_table, [column], [ref_column], ondelete='SET NULL')


def downgrade() -> None:
    connection = op.get_bind()

    for table, column, ref_table, ref_column in _CASCADE_FKS + _SET_NULL_FKS:
        name = _existing_fk_name(connection, table, column)
        op.drop_constraint(name, table, type_='foreignkey')
        op.create_foreign_key(name, table, ref_table, [column], [ref_column])
