from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Коллбек с типом данных для фильтра
class MyCallback(CallbackData, prefix = 'my'):
    foo: str


def start_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Создать сделку',
            callback_data=MyCallback(foo='Bitrix24').pack())
    )
    return builder.as_markup()


"""
start_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Создать заказ на Битрикс24',
            callback_data=MyCallback(foo='Bitrix24')
        )
    ],
    [
        InlineKeyboardButton(
            text='Место для других функций',
            callback_data='Button2'
        )
    ]
])
"""

