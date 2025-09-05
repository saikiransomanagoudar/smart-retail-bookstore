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
    from sqlalchemy import text
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Add missing columns safely for existing tables
    try:
        with engine.connect() as conn:
            # Check if themes_of_interest column exists (PostgreSQL syntax)
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'user_preferences'"
            ))
            columns = [row[0] for row in result.fetchall()]
            
            if 'themes_of_interest' not in columns:
                conn.execute(text("ALTER TABLE user_preferences ADD COLUMN themes_of_interest TEXT"))
                conn.commit()
                print("✅ Added themes_of_interest column")
    except Exception as e:
        print(f"ℹ️  Column update not needed or failed: {e}")
