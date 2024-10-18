from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from asyncpg.pool import Pool


menu_router = Router()


@menu_router.message(Command('menu'))
async def menu(message: Message) -> None:
    '''
    обработчик команды /menu, создает главное меню и отсылает пользователю
    '''

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
            [InlineKeyboardButton(text='отменить ставку',
                                  callback_data='del')],
            [InlineKeyboardButton(text='удалить стратегию',
                                  callback_data='del_strat')]
                                  ])
    # добавить и убрать деньги

    await message.answer(text='menu',
                         reply_markup=kb)


@menu_router.callback_query(F.data == 'info')
async def info(cb: CallbackQuery, db: Pool):
    '''
    передает информацию о статегиях пользователю
    '''
    await cb.answer()
    data = await db.fetch('''
                          SELECT *
                          FROM "Strats"
                          WHERE user_tg_id=$1
                          ''', cb.from_user.id)

    await cb.message.answer(str(data))


@menu_router.message(Command('cancel'))
async def reset(message: Message, state: FSMContext) -> None:
    '''
    сбрасывает состояние fsm
    '''
    await state.clear()
    await message.answer('отменено')
