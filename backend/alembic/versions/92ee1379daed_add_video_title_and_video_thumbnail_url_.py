from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '92ee1379daed'
down_revision: Union[str, None] = '80498917cc7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('analysis_jobs', sa.Column('video_title', sa.Unicode(length=500), nullable=True))
    op.add_column('analysis_jobs', sa.Column('video_thumbnail_url', sa.String(length=2048), nullable=True))


def downgrade() -> None:
    op.drop_column('analysis_jobs', 'video_thumbnail_url')
    op.drop_column('analysis_jobs', 'video_title')
