'''config.py'''
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    personal_access_token: str
    organization_url: str
    query_id: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()