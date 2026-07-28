from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '17e0eb8c2b38'
down_revision: Union[str, None] = 'd9e7d3758050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('analysis_jobs', sa.Column('total_fetched_comments', sa.Integer(), nullable=True))
    op.add_column('analysis_jobs', sa.Column('total_cleaned_comments', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('analysis_jobs', 'total_cleaned_comments')
    op.drop_column('analysis_jobs', 'total_fetched_comments')
