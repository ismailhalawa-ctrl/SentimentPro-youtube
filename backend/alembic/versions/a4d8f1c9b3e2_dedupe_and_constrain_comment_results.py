from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a4d8f1c9b3e2'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                PARTITION BY job_id, comment_id, capability
                ORDER BY created_at DESC, id DESC
            ) AS rn
            FROM comment_analysis_results
        )
        DELETE FROM ranked WHERE rn > 1
        """
    )
    op.create_unique_constraint(
        "uq_comment_results_job_comment_capability",
        "comment_analysis_results",
        ["job_id", "comment_id", "capability"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_comment_results_job_comment_capability",
        "comment_analysis_results",
        type_="unique",
    )
