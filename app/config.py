from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Use the project's .env file in the app folder
    model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))

    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expiration_time_in_minutes: int

settings = Settings() #type: ignore