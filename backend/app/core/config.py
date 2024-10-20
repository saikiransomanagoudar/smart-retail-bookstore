from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Recommendation System"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://postgres:admin@localhost/book_recommendations"  # Default to a SQLite database
    OPENAI_API_KEY: str
    HARDCOVER_API_URL: str = "https://api.hardcover.app/v1/graphql"
    HARDCOVER_API_TOKEN: str = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiNiIsImlkIjoxOTY2MCwibG9nZ2VkSW4iOnRydWUsInN1YiI6IjE5NjYwIiwiaWF0IjoxNzI4ODY1MTk4LCJleHAiOjE3NjAzMTUwOTgsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiIxOTY2MCJ9fQ.o_RvVPhf-Jwl9nc0q7_en1liv85nXQLN1lPEjXP-_bI"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

settings = Settings()

print(f"Loaded settings: DATABASE_URL={settings.DATABASE_URL}, HARDCOVER_API_URL={settings.HARDCOVER_API_URL}, OPENAI-KEY={settings.OPENAI_API_KEY}")