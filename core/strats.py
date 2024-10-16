from aiogram import Router
from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext
from asyncpg.pool import Pool

from state_machines import StrategyInsertionFSM

strats_router = Router()


@strats_router.message(StrategyInsertionFSM.description)
async def description(message: Message, state: FSMContext) -> None:
    # добавить валидацию
    await state.set_data({'description': message.text})
    await state.set_state(StrategyInsertionFSM.balance)
    await message.answer('введите баланс')


@strats_router.message(StrategyInsertionFSM.balance)
async def balance(message: Message, state: FSMContext) -> None:
    # добавить валидацию
    data = {}
    data['balance'] = int(message.text)

    await state.update_data(data)

    await message.answer('введите название стратегии')
    await state.set_state(StrategyInsertionFSM.title)


@strats_router.message(StrategyInsertionFSM.title)
async def title(message: Message, state: FSMContext, db: Pool) -> None:
    # добавить валидацию
    data = await state.get_data()
    # здесь sql и try except
    await db.execute('''
                     INSERT INTO "Strats"
                     (user_tg_id, description, balance, title)
                     VALUES ($1, $2, $3, $4)
                     ''', message.from_user.id, data['description'], data['balance'], message.text)
    await message.answer('успешно')
    await state.set_state()
