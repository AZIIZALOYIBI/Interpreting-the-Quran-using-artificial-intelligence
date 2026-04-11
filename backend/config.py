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
    # vLLM server — set to the base URL of a running vLLM OpenAI-compatible server.
    # Example: "http://localhost:8080/v1"
    # Serves GLM-4.7-FP8 (or any model) with the OpenAI-compatible API.
    # Start the server with:
    #   vllm serve zai-org/GLM-4.7-FP8 \
    #       --tensor-parallel-size 4 \
    #       --speculative-config.method mtp \
    #       --speculative-config.num_speculative_tokens 1 \
    #       --tool-call-parser glm47 \
    #       --reasoning-parser glm45 \
    #       --enable-auto-tool-choice \
    #       --served-model-name glm-4.7-fp8
    VLLM_BASE_URL: str = ""
    # The model name as registered with --served-model-name in the vLLM server.
    VLLM_MODEL_NAME: str = "glm-4.7-fp8"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
