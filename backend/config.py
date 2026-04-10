from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://quran_user:secure_password_here@db:5432/quran_ai"
    REDIS_URL: str = "redis://redis:6379/0"
    OPENAI_API_KEY: str = ""
    PINECONE_API_KEY: str = ""
    PINECONE_ENV: str = ""
    CORS_ORIGINS: str = "http://localhost:3000"
    # Local GPTQ model — set to a HuggingFace repo ID or absolute local path.
    # Example: "TheBloke/WizardCoder-15B-1.0-GPTQ"
    # Leave empty to skip local inference and use mock responses instead.
    GPTQ_MODEL_PATH: str = ""
    # Enable Triton kernels for faster GPTQ inference (requires triton package).
    GPTQ_USE_TRITON: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
