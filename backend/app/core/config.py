import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(__file__)
backend_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

env_path = os.path.join(backend_root, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    DATABASE_URL: str
    OPENAI_API_KEY: str
    HARDCOVER_API_URL: str
    HARDCOVER_API_TOKEN: str

    class Config:
        env_file = None
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()

