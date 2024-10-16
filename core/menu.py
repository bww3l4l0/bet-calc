from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from asyncpg.pool import Pool

from state_machines import StrategyInsertionFSM, NewBetFSM


menu_router = Router()


@menu_router.message(Command('menu'))
async def menu(message: Message) -> None:

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='добавить новую стратегию',
                                  callback_data='new')],
            [InlineKeyboardButton(text='информация о статегиях',
                                  callback_data='info')],
            [InlineKeyboardButton(text='добавить ставку',
                                  callback_data='bet')],
            [InlineKeyboardButton(text='закрыть ставку',
                                  callback_data='close')],
            [InlineKeyboardButton(text='удалить стратегию',
                                  callback_data='del')]])
    # добавить и убрать деньги

    await message.answer(text='menu',
                         reply_markup=kb)


@menu_router.callback_query(F.data == 'new')
async def new(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(StrategyInsertionFSM.description)
    await cb.message.answer('введите описание стратегии')


@menu_router.callback_query(F.data == 'info')
async def info(cb: CallbackQuery, db: Pool):
    await cb.answer()
    data = await db.fetch('''
                          SELECT *
                          FROM "Strats"
                          WHERE user_tg_id=$1
                          ''', cb.from_user.id)

    await cb.message.answer(str(data))


@menu_router.callback_query(F.data == 'bet')
async def bet(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(NewBetFSM.description)
    await cb.message.answer('введите описание ставки')


@menu_router.callback_query(F.data == 'close')
async def close(cb: CallbackQuery):
    pass


@menu_router.callback_query(F.data == 'del')
async def delete(cb: CallbackQuery):
    pass
