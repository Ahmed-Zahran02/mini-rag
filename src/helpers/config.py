from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Define the settings schema
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int  # in MB
    DATA_DIR: Path
    CHUNK_SIZE: int  # 500 KB
    DATABASE_URL: str
    DATABASE_NAME: str

    GENERATION_BACKEND="OPENAI"
    EMBEDDING_BACKEND="COHERE"
    OPENAI_API_URL: str 
    COHERE_API_KEY: str

    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_SIZE:int

    INPUT_MAX_CHARACTERS:int
    GENERATION_MAX_TOKENS:int
    GENERATION_TEMPERATURE:int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    return Settings()
