from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'b71e4f2a8c15'
down_revision: Union[str, None] = 'a3d8f61c9e42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_comment_analyses_job_id', table_name='comment_analyses')
    op.create_index(
        'ix_comment_analyses_job_id_like_count',
        'comment_analyses',
        ['job_id', 'like_count'],
        unique=False,
    )

def downgrade() -> None:
    op.drop_index('ix_comment_analyses_job_id_like_count', table_name='comment_analyses')
    op.create_index(
        op.f('ix_comment_analyses_job_id'), 'comment_analyses', ['job_id'], unique=False
    )
