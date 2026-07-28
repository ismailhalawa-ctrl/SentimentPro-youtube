from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

revision: str = 'b7e1f4a8c6d3'
down_revision: Union[str, None] = 'a4d8f1c9b3e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_datetime_type = sa.DateTime().with_variant(mssql.DATETIME2, "mssql")


def upgrade() -> None:
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('tier', sa.String(length=32), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('stripe_customer_id', sa.String(length=255), nullable=True),
        sa.Column('stripe_subscription_id', sa.String(length=255), nullable=True),
        sa.Column('current_period_end', _datetime_type, nullable=True),
        sa.Column('created_at', _datetime_type, nullable=False),
        sa.Column('updated_at', _datetime_type, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index('ix_subscriptions_stripe_customer_id', 'subscriptions', ['stripe_customer_id'])
    op.create_index('ix_subscriptions_stripe_subscription_id', 'subscriptions', ['stripe_subscription_id'])

    op.create_table(
        'support_messages',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('name', sa.Unicode(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Unicode(length=4000), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('created_at', _datetime_type, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_support_messages_user_id', 'support_messages', ['user_id'])
    op.create_index('ix_support_messages_email', 'support_messages', ['email'])
    op.create_index('ix_support_messages_created_at', 'support_messages', ['created_at'])


def downgrade() -> None:
    op.drop_table('support_messages')
    op.drop_table('subscriptions')
