from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision: str = 'ef063169c7c5'
down_revision: Union[str, None] = 'c2b3ab599189'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('embedding_indexes',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('job_id', sa.BigInteger(), nullable=False),
    sa.Column('embedding_provider_id', sa.String(length=64), nullable=False),
    sa.Column('vector_store_provider_id', sa.String(length=64), nullable=False),
    sa.Column('vector_count', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'COMPLETE', 'FAILED', name='embeddingindexstatus', native_enum=False, length=20), nullable=False),
    sa.Column('error_message', sa.String(length=1024), nullable=True),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.Column('updated_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['analysis_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_embedding_indexes_job_id'), 'embedding_indexes', ['job_id'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_embedding_indexes_job_id'), table_name='embedding_indexes')
    op.drop_table('embedding_indexes')
