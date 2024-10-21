from aiogram import Router, F
from aiogram.types.message import Message
from aiogram.types.callback_query import CallbackQuery

from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from aiogram.fsm.context import FSMContext


from asyncpg.pool import Pool

from core.state_machines import NewBetFSM
from core.models import StrategyCallbackData

new_bet_router = Router()


async def reset(message: Message,
                error_text: str,
                state: FSMContext
                ) -> None:
    '''reset fsm state and send error message
    '''
    await message.answer(error_text,
                         protect_content=True)
    await state.clear()


@new_bet_router.callback_query(F.data == 'bet')
async def bet(cb: CallbackQuery, state: FSMContext):
    '''обработчик кнопки новая ставка из главного меню
    '''
    await cb.answer()
    await state.set_state(NewBetFSM.description)
    await cb.message.answer('введите описание ставки',
                            protect_content=True)

@new_bet_router.message(NewBetFSM.description)
async def description(message: Message,
                      state: FSMContext) -> None:
    '''
    Функция валидирует описание ставки и
    меняет состояние на NewBetFSM.coef
    '''

    await state.set_data({'description': message.text})

    await state.set_state(NewBetFSM.coef)

    await message.answer('введите коэфициент события',
                         protect_content=True)


@new_bet_router.message(NewBetFSM.coef)
async def coef(message: Message,
               state: FSMContext) -> None:
    '''
    Функция валидирует коэфициент ставки и
    меняет состояние на NewBetFSM.cash
    '''

    msg_error = '''ошибка валидации, коэфициент должен быть
    числом с плавающей точкой больше 1.0, например 1.5'''

    try:
        coeficient = float(message.text)
    except ValueError:
        await reset(message, msg_error, state)
        return

    if coeficient <= 1.0:
        await reset(message, msg_error, state)
        return

    await state.update_data(coef=coeficient)

    await state.set_state(NewBetFSM.cash)

    await message.answer('введите размер ставки',
                         protect_content=True)


@new_bet_router.message(NewBetFSM.cash)
async def cash(message: Message,
               state: FSMContext,
               db: Pool) -> None:
    '''
    Функция валидирует размер ставки,
    создает клавиатуру выбора статегии и
    меняет состояние на NewBetFSM.strategy_id_p1
    '''

    msg_text = 'сумма должна быть целым положительным числом'

    try:
        data = int(message.text)
    except ValueError:
        await reset(message, msg_text, state)
        return

    if data < 1:
        await reset(message, msg_text, state)
        return

    await state.update_data(cash=data)

    strats = await db.fetch('''
                            SELECT id, title
                            FROM "Strats"
                            WHERE user_tg_id=$1
                            ''', message.from_user.id)

    buttons = []

    for strat in strats:
        buttons.append([InlineKeyboardButton(text=strat['title'],
                                             callback_data=StrategyCallbackData(id=strat['id']).pack())])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer('выберете стратегию', reply_markup=kb,
                         protect_content=True)

    await state.set_state(NewBetFSM.strategy_id_p1)


@new_bet_router.callback_query(StrategyCallbackData.filter())
async def kb_handler(cb: CallbackQuery,
                     callback_data: StrategyCallbackData,
                     db: Pool,
                     state: FSMContext) -> None:
    '''вставка информации о новой ставке в бд
    '''
    await cb.answer()
    fsm_data = await state.get_data()

    # если fsm пустой то значит что это старая уже использованая клавиатура и нужно пройти все этапы заново
    if not bool(fsm_data):
        await cb.message.answer('ставка уже была добавленая ранее')
        return

    # try except
    await db.execute('''
                     INSERT INTO "Bets" (bet, coef, cash_amount, strat_id)
                     VALUES ($1, $2, $3, $4)
                     ''',
                     fsm_data['description'], fsm_data['coef'], fsm_data['cash'], callback_data.id)

    await state.clear()

    await cb.message.answer('успешно',
                            protect_content=True)
