from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_TIMEOUT: int = 30

    INVENTORY_API_BASE_URL: str
    INVENTORY_TIMEOUT: int = 10

    class Config:
        env_file = ".env"


settings = Settings()