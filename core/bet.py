from aiogram import Router
from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from state_machines import NewBetFSM

new_bet_router = Router()


@new_bet_router.message(NewBetFSM.description)
async def description(message: Message, state: FSMContext) -> None:
    # валидация
    await state.set_data({'description': message.text})
    await state.set_state(NewBetFSM.coef)
    await message.answer('введите коэфициент события')


@new_bet_router.message(NewBetFSM.coef)
async def coef(message: Message, state: FSMContext) -> None:
    await state.update_data(coef=message.text)
    await message.answer('введите размер ставки')
    await state.set_state(NewBetFSM.cash)


@new_bet_router.message(NewBetFSM.cash)
async def cash(message: Message, state: FSMContext) -> None:
    print(await state.get_data())
