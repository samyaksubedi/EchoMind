from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# ───────────────────────────────────────────
# Add server/ to sys.path so we can import app
# without this, "from app.config import settings" fails
# because Python doesn't know where app/ lives
# ───────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.databases.postgres_db import Base

# import all models so Base.metadata knows about them
# without these imports Base.metadata is empty → generates empty migration!
from app.models.models import User, Conversation, Message, UserSession

# ───────────────────────────────────────────
# Alembic Config object — access to alembic.ini values
# ───────────────────────────────────────────
config = context.config

# set DB URL from our .env via settings
# overrides the sqlalchemy.url in alembic.ini
config.set_main_option("sqlalchemy.url", settings.get_database_url)

# setup alembic's own logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Base.metadata = registry of all our models/tables
# alembic compares this against actual DB to find differences
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    offline mode — generates SQL without connecting to DB
    useful for reviewing SQL before running
    triggered by: alembic upgrade head --sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    online mode — connects to DB and runs migrations directly
    this is what we use 99% of the time
    triggered by: alembic upgrade head
    """
    # create engine using sqlalchemy.url we set above
    # NullPool — no connection pooling needed for migrations
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # our models
        )

        with context.begin_transaction():
            context.run_migrations()  # runs upgrade() or downgrade()


# decide which mode based on how alembic command was run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
