from alembic import command
from sqlalchemy import select

from app.models import Priority


class TestMigrations:
    def test_default_priorities_seeded(self, db_session):
        names = db_session.scalars(select(Priority.name)).all()

        assert sorted(names) == ["High", "Low", "Medium"]

    def test_models_match_migrations(self, alembic_config):
        command.check(alembic_config)

    def test_downgrade_and_upgrade(self, alembic_config):
        command.downgrade(alembic_config, "base")
        command.upgrade(alembic_config, "head")
