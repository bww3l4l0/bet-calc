from os import getenv

from pydantic import PostgresDsn, Field, IPvAnyAddress
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str = getenv('TOKEN')
    POSTGRESDSN: PostgresDsn = getenv('POSTGRESDSN')


settings = Settings()
