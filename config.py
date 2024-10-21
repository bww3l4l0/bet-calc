from os import getenv
from typing import Literal

from pydantic import PostgresDsn, Field, RedisDsn, field_validator
from pydantic_settings import BaseSettings
from pydantic import ValidationError
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings(BaseSettings):
    '''
    контейнер настроек с валидацией
    '''
    TOKEN: str = getenv('TOKEN')
    POSTGRES_DSN: PostgresDsn = getenv('POSTGRESDSN')
    REDIS_DSN: RedisDsn = getenv('REDISDSN')
    REDIS_TTL: int = Field(int(getenv('REDIS_TTL')), ge=10, le=3600)

    LOGGING_LEVEL: int = getenv('LOGGING_LEVEL')

    @field_validator('LOGGING_LEVEL')
    def validate_log_level(value: int) -> int:
        if value in [0, 10, 20, 30, 40, 50]:
            return value
        raise ValidationError('value must be one of 0, 10, 20, 30, 40, 50')

    LOGGING_MODE: Literal['w', 'a'] = getenv('LOGGING_MODE')


settings = Settings()
