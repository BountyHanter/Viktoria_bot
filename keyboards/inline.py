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
            callback_data=MyCallback(foo='Bitrix24').pack()),
        )
    return builder.as_markup()

# Изолированная кнопка
""" InlineKeyboardButton( # Пока что не нужен 
     text='Отобразить сделки',
     callback_data=MyCallback(foo='show_deals').pack()),"""


def add_comment_to_discussion():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить',
            callback_data=MyCallback(foo='add_comment_to_dicscussion').pack()),
        InlineKeyboardButton(
            text='Не добавлять',
            callback_data=MyCallback(foo='not_add_comment_to_dicscussion').pack()),

    )
    return builder.as_markup()

"""
def what_do_with_deal():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить комментарий',
            callback_data=MyCallback(foo='comment_deal').pack()),
        InlineKeyboardButton(
            text='Удалить сделку',
            callback_data=MyCallback(foo='delete_deal').pack()),
    )
    
"""