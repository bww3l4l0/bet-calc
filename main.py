import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from asyncpg.pool import create_pool
from redis.asyncio import Redis

from config import settings
from core.menu import menu_router
from core.strats import strats_router
from core.bet import new_bet_router
from core.opened_bets import opened_bets_router


redis = Redis(host=settings.REDIS_DSN.host,
              port=settings.REDIS_DSN.port
              )

storage = RedisStorage(redis,
                       state_ttl=settings.REDIS_TTL)

dp = Dispatcher(storage=storage)

dp.include_router(menu_router)
dp.include_router(strats_router)
dp.include_router(new_bet_router)
dp.include_router(opened_bets_router)

logging.basicConfig(level=settings.LOGGING_LEVEL,
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(filename='./logs/log.log',
                                                  mode=settings.LOGGING_MODE)])


async def main():
    '''entry point
    '''
    bot = Bot(settings.TOKEN)

    db = await create_pool(str(settings.POSTGRES_DSN))
    dp['db'] = db

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


'''todo
try except для sql
логирование
переделать на spa like
'''