from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '80498917cc7f'
down_revision: Union[str, None] = 'cb7c5b0105ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('comment_analysis_results', sa.Column('processing_time_ms', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('comment_analysis_results', 'processing_time_ms')
