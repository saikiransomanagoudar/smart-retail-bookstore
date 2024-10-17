from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings

# Create the engine using the DATABASE_URL from the settings
engine = create_engine(settings.DATABASE_URL)

# Create a sessionmaker, which will be used to create session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency to get a DB session in API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables based on models
def create_tables():
    # Import your models here
    from backend.app.models.user import UserPreferences
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
