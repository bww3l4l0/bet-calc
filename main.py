import asyncio

from aiogram import Bot, Dispatcher
from asyncpg.pool import create_pool
from pydantic import PostgresDsn

from config import settings


dp = Dispatcher()


async def main():
    bot = Bot(settings.TOKEN)
    # pg_dsn = PostgresDsn
    db = await create_pool(str(settings.POSTGRESDSN))
    dp['db'] = db

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
