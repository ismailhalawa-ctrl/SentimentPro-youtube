from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision: str = 'd9e7d3758050'
down_revision: Union[str, None] = '56b437a10168'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('assistant_sessions',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.Column('updated_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assistant_sessions_user_id'), 'assistant_sessions', ['user_id'], unique=False)
    op.create_table('assistant_messages',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('session_id', sa.BigInteger(), nullable=False),
    sa.Column('role', sa.String(length=16), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.Column('citations_json', sa.JSON(), nullable=False),
    sa.Column('tool_calls_json', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['assistant_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assistant_messages_session_id'), 'assistant_messages', ['session_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_assistant_messages_session_id'), table_name='assistant_messages')
    op.drop_table('assistant_messages')
    op.drop_index(op.f('ix_assistant_sessions_user_id'), table_name='assistant_sessions')
    op.drop_table('assistant_sessions')
