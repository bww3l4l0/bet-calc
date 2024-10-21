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
                         reply_markup=kb,
                         protect_content=True)


@menu_router.callback_query(F.data == 'info')
async def info(cb: CallbackQuery, db: Pool):
    '''
    передает информацию о статегиях пользователю
    '''
    await cb.answer()

    data = await db.fetch('''
                            WITH tab AS(
                            SELECT 	strat_id,
                                    id,
                                    (case when outcome then coef * cash_amount
                                    when not outcome then -cash_amount
                                    end) AS result
                            FROM "Bets")
                            SELECT  title,
                                    result
                            FROM(SELECT strat_id, sum(result) AS result
                                FROM tab
                                GROUP BY strat_id)
                            JOIN "Strats" s on s.id=strat_id
                            WHERE user_tg_id=$1
                          ''',
                          cb.from_user.id)

    await cb.message.answer(str(data),
                            protect_content=True)


@menu_router.message(Command('cancel'))
async def reset(message: Message, state: FSMContext) -> None:
    '''
    сбрасывает состояние fsm
    '''
    await state.clear()
    await message.answer('отменено',
                         protect_content=True)
