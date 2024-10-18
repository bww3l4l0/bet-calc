import asyncio

from asyncpg.pool import create_pool, Pool

from config import settings



'''
стратегии пользователя
select *
from "Strats"
where user_tg_id=993955495
'''


"""await db.execute('''INSERT INTO "Strats"
(user_tg_id, description, balance, title)
                     VALUES ($1, $2, $3, $4)
                     ''', 993955495, 'aaa', 800, 'test strat')"""


"""
вставка новой ставки
await db.execute('''
                     INSERT INTO "Bets"
                     (bet, coef, cash_amount, strat_id)
                     VALUES ($1, $2, $3, $4)
                     ''', 'победа красных', 1.6, 55, 2)
"""


async def main():

    db = Pool(str(settings.POSTGRESDSN))

    res = await db.fetch('''
                         SELECT *
                         FROM "Strats"
                         ''')

    print(res)

    res = await db.fetch('''
                         SELECT *
                         FROM "Bets"
                         ''')

    await db.execute('''
                     INSERT INTO "Bets"
                     (bet, coef, cash_amount, strat_id)
                     VALUES ($1, $2, $3, $4)
                     ''', 'победа красных', 1.6, 55, 2)

    print(res)


if __name__ == '__main__':
    # asyncio.run(main())
    float('1,5')
