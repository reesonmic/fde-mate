from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.config.settings import settings

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url

# Import all models so they're registered in Base.metadata
from app.models.base import Base
from app.models.user import User  # noqa: F401
from app.models.task import Task, TaskHistory  # noqa: F401
from app.models.project import Project, ProjectMember, Milestone, Risk  # noqa: F401
from app.models.customer import Customer, Contact, Opportunity  # noqa: F401
from app.models.file import FileMeta  # noqa: F401
from app.models.coach import BestPractice, Sop, LearningPath, Chapter, UserChapterProgress  # noqa: F401
from app.models.ai import AiSession, AiMessage  # noqa: F401

# this is the Alembic Config object
config = context.config

# Get DB URL and convert async driver to sync for alembic
_raw_url = settings.database_url
_url = make_url(_raw_url)
if _url.drivername.startswith("mysql+aiomysql"):
    _url = _url.set(drivername="mysql+pymysql")

# Extract charset from query string and pass via connect_args instead
_charset = _url.query.get("charset") or _url.query.get("charset=utf8mb4")
_clean_url = _url._replace(query=None) if _url.query else _url

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=True)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connect_args = {"charset": "utf8mb4"} if _charset else {}
    connectable = create_engine(_clean_url, poolclass=pool.NullPool, connect_args=connect_args)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
