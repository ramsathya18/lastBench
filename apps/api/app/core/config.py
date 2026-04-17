from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Learning Platform API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite+pysqlite:///./app.db"
    api_secret_key: str = "dev-secret"
    api_refresh_secret_key: str = "dev-refresh"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


settings = Settings()
