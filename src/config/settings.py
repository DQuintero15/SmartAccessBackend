from pydantic_settings import BaseSettings

from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    firebase_credential_path: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    basic_auth_user: str
    basic_auth_password: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()

@lru_cache()
def get_settings():
    return settings