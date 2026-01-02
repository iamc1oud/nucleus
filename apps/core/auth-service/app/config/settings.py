from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "nucleus"
    DB_PASSWORD: str = "nucleus"
    DB_NAME: str = "nucleus"

    ISSUER: str = "https://nucleus.example.com"
    KID: str = "nucleus-auth-1"
    JWKS_URL: str = "http://localhost:8000/.well-known/jwks.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
