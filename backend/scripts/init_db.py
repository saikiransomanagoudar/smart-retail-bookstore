#!/usr/bin/env python3
"""
Database initialization script for production deployment.
This script creates all necessary tables and can be run after deployment.
"""
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.database.database import create_tables, engine
from app.models.user import UserPreferences
from app.models.orders import Order
from sqlalchemy import text

def init_database():
    """Initialize the database with all required tables."""
    try:
        print("🔧 Initializing database...")
        
        # Test database connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Create all tables
        create_tables()
        print("✅ Database tables created successfully")
        
        print("🎉 Database initialization completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
