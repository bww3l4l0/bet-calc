import json
from os import getenv

from pydantic import PostgresDsn, Field, IPvAnyAddress, RedisDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    '''
    контейнер настроек
    '''
    TOKEN: str = getenv('TOKEN')
    POSTGRES_DSN: PostgresDsn = getenv('POSTGRESDSN')
    REDIS_DSN: RedisDsn = getenv('REDISDSN')
    # REDIS_TTL: Field = Field(int(getenv('REDIS_TTL')), ge=10, le=3600)
    REDIS_TTL: int = int(getenv('REDIS_TTL'))


settings = Settings()
