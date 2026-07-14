from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/reliabilityhub"
    PROJECT_NAME: str = "Reliability Hub"
    API_PORT: int = 8003

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
