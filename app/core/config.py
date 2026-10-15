from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str | None = None
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5

    class Config:
        env_file = ".env"

settings = Settings()