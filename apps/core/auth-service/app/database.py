from sqlmodel import SQLModel, create_engine, Session
from functools import lru_cache
from .config.settings import Settings

# Global engine variable
engine = None

@lru_cache
def get_settings():
    return Settings()

def get_database_url() -> str:
    """Construct database URL from settings"""
    settings = get_settings()
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

def create_db_engine():
    """Create and return SQLModel engine"""
    database_url = get_database_url()
    return create_engine(database_url, echo=True)

def init_db():
    """Initialize database connection (migrations handle schema)"""
    global engine
    engine = create_db_engine()
    # Note: Table creation is now handled by Alembic migrations
    # Run: alembic upgrade head

def get_session():
    """Get database session"""
    global engine
    if engine is None:
        engine = create_db_engine()
    
    with Session(engine) as session:
        yield session

def get_engine():
    """Get database engine"""
    global engine
    if engine is None:
        engine = create_db_engine()
    return engine