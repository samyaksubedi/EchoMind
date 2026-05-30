from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Engine — the actual connection to PostgreSQL
engine = create_engine(
    settings.get_database_url,
    echo=settings.APP_ENV == "development",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# sessionmaker is a class that generates new Session objects when called
# so on each req we get a new sessionmaker's instance which is indeed
# the session that is independent of others
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# declarative_base() is a factory function that constructs a base class
# for declarative class definitions. All models inherit from this Base class
# which provides SQLAlchemy functionality to map Python classes to DB tables
Base = declarative_base()


def test_postgres_conn() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("PostgreSQL connected ")
        return True
    except SQLAlchemyError as e:
        logger.error(f"PostgreSQL connection failed : {e}")
        return False


# On each request get_db is called by dependency injection
# it creates a new session, yields it to the route handler
# and ensures it's closed after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()
