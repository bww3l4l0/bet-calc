from typing import Literal
from aiogram.filters.callback_data import CallbackData


class StrategyCallbackData(CallbackData, prefix='s'):
    '''
    модель для передачи id стратегии
    '''
    id: int


class BetClosingData(CallbackData, prefix='c'):
    '''
    модель для удаления или закрытия ставки
    '''
    action: Literal['close', 'delete']
    id: int


class BetResultData(CallbackData, prefix='r'):
    '''
    модель для передачи результата ставки
    '''
    id: int
    result: bool


class StrategyDeletionData(CallbackData, prefix='sd'):
    '''
    модель для удаления статегии
    '''
    id: int
