from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Recommendation System"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:admin@localhost/book_recommendations"  # Default to a SQLite database
    OPENAI_API_KEY: str
    HARDCOVER_API_URL: str = "https://api.hardcover.app/v1/graphql"  # Default Hardcover API URL

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

settings = Settings()

print(f"Loaded settings: DATABASE_URL={settings.DATABASE_URL}, HARDCOVER_API_URL={settings.HARDCOVER_API_URL}")