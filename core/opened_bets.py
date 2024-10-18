from aiogram import Router, F

from asyncpg.pool import Pool

from aiogram.types.message import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from core.models import BetClosingData, BetResultData

opened_bets_router = Router()


@opened_bets_router.callback_query(F.data == 'close')
@opened_bets_router.callback_query(F.data == 'del')
async def close(cb: CallbackQuery, db: Pool):
    '''
    обрабатывает события закрытие ставки и отмена ставки
    '''
    await cb.answer()
    bets = await db.fetch('''
                          SELECT id, bet
                          FROM "Bets"
                          WHERE outcome is null
                          ''')

    buttons = []

    if cb.data == 'close':

        for bet in bets:
            buttons.append([
                InlineKeyboardButton(text=bet['bet'],
                                     callback_data=BetClosingData(id=bet['id'], action='close').pack())
            ])

    elif cb.data == 'del':
        for bet in bets:
            buttons.append([
                InlineKeyboardButton(text=bet['bet'],
                                     callback_data=BetClosingData(id=bet['id'], action='delete').pack())
            ])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if not buttons:
        await cb.message.answer('открытых ставок нет')
        return

    await cb.message.answer(text='выберите ставку', reply_markup=kb)


@opened_bets_router.callback_query(BetClosingData.filter(F.action == 'delete'))
async def delete_bet(cb: CallbackQuery,
                     callback_data: BetClosingData,
                     db: Pool) -> None:
    '''
    удаляет ставку из бд
    '''

    await cb.answer()
    await db.execute('''
                     DELETE FROM "Bets"
                     WHERE id=$1
                     ''',
                     callback_data.id)

    await cb.message.answer('удалено')


@opened_bets_router.callback_query(BetClosingData.filter(F.action == 'close'))
async def close_bet(cb: CallbackQuery,
                    callback_data: BetClosingData) -> None:
    '''
    обработчик закрытия ставки
    '''

    await cb.answer()
    buttons = [[InlineKeyboardButton(text='исход положительный',
                                     callback_data=BetResultData(id=callback_data.id, result=True).pack())],
               [InlineKeyboardButton(text='исход отрицательный',
                                     callback_data=BetResultData(id=callback_data.id, result=False).pack())]]

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await cb.message.answer('исход ставки', reply_markup=kb)


@opened_bets_router.callback_query(BetResultData.filter())
async def close_bet_(cb: CallbackQuery,
                     callback_data: BetResultData,
                     db: Pool) -> None:
    '''
    получает исход ставки и измененяет соответствующих данных в бд
    '''

    await cb.answer()

    await db.execute('''
                     UPDATE "Bets"
                     SET outcome=$1
                     WHERE id=$2
                     ''', callback_data.result, callback_data.id)

    await cb.message.answer('ставка закрыта')
