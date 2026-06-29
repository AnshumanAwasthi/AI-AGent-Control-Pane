from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_env: str
    debug: bool
    api_v1_prefix: str
    database_url: str
    agents_table_name: str
    tenant_max_agents: int
    jwt_secret_key: str
    jwt_algorithm: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
