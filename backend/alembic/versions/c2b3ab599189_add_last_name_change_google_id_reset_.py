from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision: str = 'c2b3ab599189'
down_revision: Union[str, None] = 'f2e7606e7adf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('last_name_change', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=True))
    op.add_column('users', sa.Column('google_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('reset_token_hash', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=True))
    op.create_index(
        op.f('ix_users_google_id'), 'users', ['google_id'], unique=True,
        mssql_where=sa.text('google_id IS NOT NULL'),
    )
    op.create_index(op.f('ix_users_reset_token_hash'), 'users', ['reset_token_hash'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_users_reset_token_hash'), table_name='users')
    op.drop_index(op.f('ix_users_google_id'), table_name='users')
    op.drop_column('users', 'reset_token_expires_at')
    op.drop_column('users', 'reset_token_hash')
    op.drop_column('users', 'google_id')
    op.drop_column('users', 'last_name_change')
