from aiogram.fsm.state import State, StatesGroup


class StrategyInsertionFSM(StatesGroup):
    description = State()
    balance = State()
    title = State()


class NewBetFSM(StatesGroup):
    description = State()
    coef = State()
    cash = State()
    strategy_id_p1 = State()
    strategy_id_p2 = State()
