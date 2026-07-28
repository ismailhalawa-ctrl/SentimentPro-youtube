from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a3d8f61c9e42'
down_revision: Union[str, None] = 'c8f3a1d7e5b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_job_insights_job_capability', table_name='job_insights')
    op.create_unique_constraint(
        'uq_job_insights_job_capability', 'job_insights', ['job_id', 'capability']
    )

def downgrade() -> None:
    op.drop_constraint('uq_job_insights_job_capability', 'job_insights', type_='unique')
    op.create_index(
        'ix_job_insights_job_capability', 'job_insights', ['job_id', 'capability'], unique=False
    )
