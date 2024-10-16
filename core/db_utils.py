import asyncio

from asyncpg import Record
from asyncpg.pool import Pool

from config import settings


class DBWraper(Pool):
    def __init__(self, *connect_args, min_size, max_size, max_queries,
                 max_inactive_connection_lifetime, setup, init, loop, connection_class,
                 record_class, **connect_kwargs):
        super().__init__(*connect_args, min_size=min_size, max_size=max_size, max_queries=max_queries,
                         max_inactive_connection_lifetime=max_inactive_connection_lifetime, setup=setup,
                         init=init, loop=loop, connection_class=connection_class, record_class=record_class, **connect_kwargs)


def get_all_strats(db: Pool,
                   tg_id: int) -> list[Record]:
    pass


def get_opened_bets(db: Pool,
                    tg_id: int) -> list[Record]:
    pass


def insert_strat(db: Pool,
                 description: str,
                 user_tg_id: str,
                 begining_balance: float,
                 title: str) -> None:
    pass


def insert_bet(db: Pool,
               strat_id: int,
               description: str,
               cf: float,
               cash: float) -> None:
    pass


def set_outcome(db: Pool,
                bet_id: int,
                outcome: bool) -> None:
    pass


def main():
    pool = Pool(str(settings.POSTGRESDSN))
    

if __name__ == '__main__':
    asyncio.run(main())