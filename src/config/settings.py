from pydantic_settings import BaseSettings

from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    supabase_url: str
    supabase_key: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()

@lru_cache()
def get_settings():
    return settings