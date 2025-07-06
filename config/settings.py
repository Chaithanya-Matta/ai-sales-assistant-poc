from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "addresses")
    POSTGRES_DB_USER: str = os.getenv("POSTGRES_DB_USER")
    POSTGRES_DB_PASSWORD: str = os.getenv("POSTGRES_DB_PASSWORD")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", 1.0))
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL")

    class Config:
        env_file = ".env"  # Optional: Automatically loads from .env

settings = Settings()