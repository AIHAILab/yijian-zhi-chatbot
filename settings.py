from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # Data source
    data_source_original_dir: str = "data_source/original"
    data_source_splitted_dir: str = "data_source/splitted"
    vector_store_dir: str = "qdrant"

    # Langsmith
    langsmith_tracing: bool = False
    langsmith_endpoint: str | None = "https://api.smith.langchain.com"
    langsmith_project: str | None = "yijian-zhi-chatbot"
    langsmith_api_key: str | None = None

    # OpenAI
    openai_api_key: str
    embedding_model: str = "text-embedding-3-large"
    llm_model: str = "gpt-4o-mini"
    dimensions: int = 3072

    # Server
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()  # type: ignore[missing-required-argument]
