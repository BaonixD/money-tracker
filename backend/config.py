from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Money Tracker"
    DB_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30
    REFRESH_SECRET_KEY: str


    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

