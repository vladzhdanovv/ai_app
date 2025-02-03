from functools import lru_cache
from pydantic_settings import BaseSettings

DEFAULT_APP_NAME = "AI APP"
DEFAULT_TOKEN_EXPIRY = 60

class Settings(BaseSettings):
    app_name: str = DEFAULT_APP_NAME
    app_description: str
    api_prefix: str
    redis_endpoint: str
    redis_port: str
    openai_api_key: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket: str
    aws_table: str
    mongo_uri: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = DEFAULT_TOKEN_EXPIRY

@lru_cache
def get_config() -> Settings:
    return Settings()
