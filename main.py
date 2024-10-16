import asyncio

from aiogram import Bot, Dispatcher
from asyncpg.pool import create_pool

from config import settings
from core.menu import menu_router
from core.strats import strats_router
from core.bet import new_bet_router


dp = Dispatcher()

dp.include_router(menu_router)
dp.include_router(strats_router)
dp.include_router(new_bet_router)


async def main():
    bot = Bot(settings.TOKEN)

    db = await create_pool(str(settings.POSTGRESDSN))
    dp['db'] = db

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
