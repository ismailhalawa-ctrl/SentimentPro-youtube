"""Add ondelete=CASCADE to assistant FKs and composite lookup indexes.

SQL Server auto-names FK constraints created without an explicit `name=`
(as the original assistant_sessions/assistant_messages migration did), so the
constraint names are not known ahead of time. This migration looks them up
from sys.foreign_keys at run time, drops them, and recreates them as named,
ON DELETE CASCADE constraints.
"""
from typing import Sequence, Union

from alembic import op

revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        DECLARE @constraint_name NVARCHAR(200);

        SELECT @constraint_name = fk.name
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.columns c
            ON fkc.parent_object_id = c.object_id AND fkc.parent_column_id = c.column_id
        WHERE fk.parent_object_id = OBJECT_ID('assistant_sessions') AND c.name = 'user_id';

        IF @constraint_name IS NOT NULL
            EXEC('ALTER TABLE assistant_sessions DROP CONSTRAINT ' + @constraint_name);

        ALTER TABLE assistant_sessions
            ADD CONSTRAINT fk_assistant_sessions_user_id
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
    """)

    op.execute("""
        DECLARE @constraint_name NVARCHAR(200);

        SELECT @constraint_name = fk.name
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.columns c
            ON fkc.parent_object_id = c.object_id AND fkc.parent_column_id = c.column_id
        WHERE fk.parent_object_id = OBJECT_ID('assistant_messages') AND c.name = 'session_id';

        IF @constraint_name IS NOT NULL
            EXEC('ALTER TABLE assistant_messages DROP CONSTRAINT ' + @constraint_name);

        ALTER TABLE assistant_messages
            ADD CONSTRAINT fk_assistant_messages_session_id
            FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE CASCADE;
    """)

    op.create_index(
        'ix_assistant_sessions_user_id_updated_at', 'assistant_sessions', ['user_id', 'updated_at'], unique=False
    )
    op.create_index(
        'ix_assistant_messages_session_id_created_at', 'assistant_messages', ['session_id', 'created_at'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index('ix_assistant_messages_session_id_created_at', table_name='assistant_messages')
    op.drop_index('ix_assistant_sessions_user_id_updated_at', table_name='assistant_sessions')

    op.execute("""
        ALTER TABLE assistant_messages DROP CONSTRAINT fk_assistant_messages_session_id;
        ALTER TABLE assistant_messages
            ADD CONSTRAINT fk_assistant_messages_session_id
            FOREIGN KEY (session_id) REFERENCES assistant_sessions(id);
    """)
    op.execute("""
        ALTER TABLE assistant_sessions DROP CONSTRAINT fk_assistant_sessions_user_id;
        ALTER TABLE assistant_sessions
            ADD CONSTRAINT fk_assistant_sessions_user_id
            FOREIGN KEY (user_id) REFERENCES users(id);
    """)
