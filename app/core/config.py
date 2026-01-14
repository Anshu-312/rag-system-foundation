from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    embedding_model: str = Field(..., env="EMBEDDING_MODEL")
    faiss_index_path: str = Field(..., env="FAISS_INDEX_PATH")

    dimension: int = Field(..., env="DIMENSION")
    chunk_size: int = Field(..., env="CHUNK_SIZE")
    chunk_overlap: int = Field(..., env="CHUNK_OVERLAP")


    openrouter_api_url: str = Field(..., env="OPENROUTER_API_URL")
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    openrouter_model: str = Field(..., env="OPENROUTER_MODEL")

    class Config:
        env_file = ".env"

settings = Settings()