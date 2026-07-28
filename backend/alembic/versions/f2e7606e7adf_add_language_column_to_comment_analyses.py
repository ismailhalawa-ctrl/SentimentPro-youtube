from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'f2e7606e7adf'
down_revision: Union[str, None] = '92ee1379daed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('comment_analyses', sa.Column('language', sa.String(length=16), nullable=True))
    op.create_index(op.f('ix_comment_analyses_language'), 'comment_analyses', ['language'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_comment_analyses_language'), table_name='comment_analyses')
    op.drop_column('comment_analyses', 'language')