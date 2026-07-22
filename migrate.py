from alembic.config import Config
from alembic import command
import os

def run_migrations():
    """Run Alembic migrations."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("✅ Migrations applied successfully!")

if __name__ == "__main__":
    run_migrations()