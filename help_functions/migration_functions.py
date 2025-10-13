import os
import sys

from conf import Logger

import alembic.config
from alembic import command


def run_migrations() -> bool:
    try:
        Logger.info("Attempting to run migrations")

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)

        alembic_cfg = alembic.config.Config(os.path.join(project_root, "alembic.ini"))

        command.upgrade(alembic_cfg, "head")

        Logger.info("Migrations have been successfully applied")
        return True


    except Exception as e:
        Logger.error(f"Error applying migrations: {e}")
        return False
