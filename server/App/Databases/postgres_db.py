from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Engine — the actual connection to PostgreSQL
engine = create_engine(
    settings.get_database_url,
    echo=settings.APP_ENV == "development",  # logs all SQL queries in dev only
    pool_pre_ping=True,  # checks connection is alive before using it
    pool_size=10,  # max 10 persistent connections
    max_overflow=20,  # 20 extra connections allowed under heavy load
)
# SessionLocal — factory that creates new sessions

#! sessionmaker is a class that generates new Session objects when called , so on each req we get a new sessionmaker's instance wich is indeed the session that is independent of others
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # we manually commit
    autoflush=False,  # we manually flush
)
# Base — parent class for all models
# declarative_base() is a factory function(a fn that return or construct objects) that constructs a base class for declarative class definitions. When we define our models, they will inherit from this Base class, which provides the necessary SQLAlchemy functionality to map our Python classes to database tables.
Base = declarative_base()


# Dependency — used in FastAPI routes via Depends()
# On each request get_db is called by dependency injection, it creates a new session, yields it to the route handler, and ensures it's closed after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
