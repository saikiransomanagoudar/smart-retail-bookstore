import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configure engine with appropriate settings for production
engine_kwargs = {}
if settings.DATABASE_URL.startswith("postgresql"):
    # PostgreSQL configuration for production
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "echo": False  # Set to True for debugging
    })
elif settings.DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine_kwargs.update({
        "check_same_thread": False,
        "echo": False
    })

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.models.user import UserPreferences
    from app.models.orders import Order

    try:
        UserPreferences.__table__.drop(engine, checkfirst=True)
    except Exception:
        pass
    
    Base.metadata.create_all(bind=engine)
