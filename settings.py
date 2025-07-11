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

    # Langsmith settings
    langsmith_tracing: bool = False
    langsmith_endpoint: str | None = "https://api.smith.langchain.com"
    langsmith_project: str | None = "yijian-zhi-chatbot"
    langsmith_api_key: str | None = None

    # LLM provider
    openai_api_key: str


settings = Settings()  # type: ignore[missing-required-argument]
