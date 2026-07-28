from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision: str = 'cb7c5b0105ac'
down_revision: Union[str, None] = 'a953d15784db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('analysis_jobs',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.Column('video_url', sa.String(length=2048), nullable=False),
    sa.Column('video_id', sa.String(length=32), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='analysisjobstatus', native_enum=False, length=20), nullable=False),
    sa.Column('progress_percentage', sa.Integer(), nullable=False),
    sa.Column('current_step', sa.Unicode(length=255), nullable=True),
    sa.Column('error_message', sa.Unicode(length=1024), nullable=True),
    sa.Column('options_json', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.Column('updated_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_jobs_owner_id'), 'analysis_jobs', ['owner_id'], unique=False)
    op.create_table('comment_analyses',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('job_id', sa.BigInteger(), nullable=False),
    sa.Column('youtube_comment_id', sa.String(length=64), nullable=False),
    sa.Column('author_display_name', sa.Unicode(length=255), nullable=False),
    sa.Column('text', sa.Unicode(length=4000), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('published_at', sa.Unicode(length=64), nullable=True),
    sa.Column('is_reply', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['analysis_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_analyses_job_id'), 'comment_analyses', ['job_id'], unique=False)
    op.create_index(op.f('ix_comment_analyses_youtube_comment_id'), 'comment_analyses', ['youtube_comment_id'], unique=False)
    op.create_table('job_insights',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('job_id', sa.BigInteger(), nullable=False),
    sa.Column('capability', sa.String(length=64), nullable=False),
    sa.Column('provider_id', sa.String(length=64), nullable=False),
    sa.Column('mode', sa.String(length=16), nullable=False),
    sa.Column('headline_label', sa.String(length=64), nullable=True),
    sa.Column('headline_score', sa.Float(), nullable=True),
    sa.Column('result_json', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['analysis_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_insights_capability'), 'job_insights', ['capability'], unique=False)
    op.create_index(op.f('ix_job_insights_headline_label'), 'job_insights', ['headline_label'], unique=False)
    op.create_index('ix_job_insights_job_capability', 'job_insights', ['job_id', 'capability'], unique=False)
    op.create_index(op.f('ix_job_insights_job_id'), 'job_insights', ['job_id'], unique=False)
    op.create_table('comment_analysis_results',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('job_id', sa.BigInteger(), nullable=False),
    sa.Column('comment_id', sa.BigInteger(), nullable=False),
    sa.Column('capability', sa.String(length=64), nullable=False),
    sa.Column('provider_id', sa.String(length=64), nullable=False),
    sa.Column('mode', sa.String(length=16), nullable=False),
    sa.Column('label', sa.String(length=64), nullable=True),
    sa.Column('confidence', sa.Float(), nullable=True),
    sa.Column('result_json', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime().with_variant(mssql.DATETIME2(), 'mssql'), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment_analyses.id'], ),
    sa.ForeignKeyConstraint(['job_id'], ['analysis_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_analysis_results_capability'), 'comment_analysis_results', ['capability'], unique=False)
    op.create_index(op.f('ix_comment_analysis_results_comment_id'), 'comment_analysis_results', ['comment_id'], unique=False)
    op.create_index(op.f('ix_comment_analysis_results_job_id'), 'comment_analysis_results', ['job_id'], unique=False)
    op.create_index(op.f('ix_comment_analysis_results_label'), 'comment_analysis_results', ['label'], unique=False)
    op.create_index('ix_comment_results_job_capability', 'comment_analysis_results', ['job_id', 'capability'], unique=False)
    op.create_index('ix_comment_results_job_label', 'comment_analysis_results', ['job_id', 'label'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_comment_results_job_label', table_name='comment_analysis_results')
    op.drop_index('ix_comment_results_job_capability', table_name='comment_analysis_results')
    op.drop_index(op.f('ix_comment_analysis_results_label'), table_name='comment_analysis_results')
    op.drop_index(op.f('ix_comment_analysis_results_job_id'), table_name='comment_analysis_results')
    op.drop_index(op.f('ix_comment_analysis_results_comment_id'), table_name='comment_analysis_results')
    op.drop_index(op.f('ix_comment_analysis_results_capability'), table_name='comment_analysis_results')
    op.drop_table('comment_analysis_results')
    op.drop_index(op.f('ix_job_insights_job_id'), table_name='job_insights')
    op.drop_index('ix_job_insights_job_capability', table_name='job_insights')
    op.drop_index(op.f('ix_job_insights_headline_label'), table_name='job_insights')
    op.drop_index(op.f('ix_job_insights_capability'), table_name='job_insights')
    op.drop_table('job_insights')
    op.drop_index(op.f('ix_comment_analyses_youtube_comment_id'), table_name='comment_analyses')
    op.drop_index(op.f('ix_comment_analyses_job_id'), table_name='comment_analyses')
    op.drop_table('comment_analyses')
    op.drop_index(op.f('ix_analysis_jobs_owner_id'), table_name='analysis_jobs')
    op.drop_table('analysis_jobs')
