from aiogram import Router, F
from aiogram.types.message import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from asyncpg.pool import Pool

from core.state_machines import StrategyInsertionFSM
from core.models import StrategyDeletionData
from core.bet import reset

strats_router = Router()


@strats_router.message(StrategyInsertionFSM.description)
async def description(message: Message, state: FSMContext) -> None:
    '''
    обработка описания при добавлении новой стратегии
    '''

    await state.set_data({'description': message.text})
    await state.set_state(StrategyInsertionFSM.balance)
    await message.answer('введите баланс')


@strats_router.message(StrategyInsertionFSM.balance)
async def balance(message: Message, state: FSMContext) -> None:
    '''
    обрабатывает введеный баланс статегии
    '''
    # добавить валидацию

    try:
        data = int(message.text)
        if data < 1:
            raise ValueError

    except ValueError:
        await reset(message, 'баланс должен быть целым числом больше ноля', state)
        return

    await state.update_data(balance=data)

    await message.answer('введите название стратегии')
    await state.set_state(StrategyInsertionFSM.title)


@strats_router.message(StrategyInsertionFSM.title)
async def title(message: Message, state: FSMContext, db: Pool) -> None:
    '''
    вставляет данные о новой стратегии в бд
    '''

    data = await state.get_data()
    # здесь sql и try except
    await db.execute('''
                     INSERT INTO "Strats"
                     (user_tg_id, description, balance, title)
                     VALUES ($1, $2, $3, $4)
                     ''', message.from_user.id, data['description'], data['balance'], message.text)
    await message.answer('успешно')
    await state.set_state()


@strats_router.callback_query(F.data == 'del_strat')
async def delete_strategy(cb: CallbackQuery, db: Pool):
    '''
    обработчик кнопки удаление стратегии из главного меню
    '''
    await cb.answer()
    strats = await db.fetch('''
                            SELECT *
                            FROM "Strats"
                            WHERE id=$1
                            ''', cb.from_user.id)
    if not strats:
        await cb.message.answer('у вас нет стратегий')
        return

    buttons = []

    for strat in strats:
        buttons.append([InlineKeyboardButton(text=strat['description'],
                                             callback_data=StrategyDeletionData(id=strat['id']))])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await cb.message.answer(text='выберите стратегию', reply_markup=kb)


@strats_router.callback_query(StrategyDeletionData.filter())
async def delete_strategy_(cb: CallbackQuery,
                           callback_data: StrategyDeletionData,
                           db: Pool) -> None:
    '''
    удаляет стратегию из бд
    '''
    await cb.answer()
    await db.execute('''
                     DELETE *
                     FROM "Strats"
                     WHERE id=$1
                     ''', callback_data.id)
    await cb.message.answer('удалено')

@strats_router.callback_query(F.data == 'new')
async def new(cb: CallbackQuery, state: FSMContext):
    '''
    обработчик кнопки новая стретегия из главного меню
    '''
    await cb.answer()
    await state.set_state(StrategyInsertionFSM.description)
    await cb.message.answer('введите описание стратегии')
