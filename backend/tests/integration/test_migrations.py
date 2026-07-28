import subprocess
import sys

from alembic.config import Config
from alembic.script import ScriptDirectory


def _alembic_config():
    return Config("alembic.ini")


def test_migration_history_is_a_single_linear_chain():
    script = ScriptDirectory.from_config(_alembic_config())
    heads = script.get_heads()
    assert len(heads) == 1, f"expected exactly one head, found {heads} (branched migration history)"


def test_migration_revisions_have_no_gaps():
    script = ScriptDirectory.from_config(_alembic_config())
    revisions = list(script.walk_revisions())
    assert len(revisions) > 0
    seen = {rev.revision for rev in revisions}
    for rev in revisions:
        if rev.down_revision is not None:
            down_revisions = (
                rev.down_revision if isinstance(rev.down_revision, tuple) else (rev.down_revision,)
            )
            for down in down_revisions:
                assert down in seen, f"revision {rev.revision} references missing parent {down}"


def test_alembic_upgrade_head_is_idempotent():
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    current = subprocess.run(
        [sys.executable, "-m", "alembic", "current"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert current.returncode == 0, current.stderr
    script = ScriptDirectory.from_config(_alembic_config())
    (head,) = script.get_heads()
    assert head in current.stdout


def test_every_revision_file_defines_upgrade_and_downgrade():
    script = ScriptDirectory.from_config(_alembic_config())
    for rev in script.walk_revisions():
        module = rev.module
        assert hasattr(module, "upgrade"), f"{rev.revision} is missing an upgrade() function"
        assert hasattr(module, "downgrade"), f"{rev.revision} is missing a downgrade() function"
        assert callable(module.upgrade)
        assert callable(module.downgrade)
