import json
import os

from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import time

import bitrix_add_company
from keyboards.inline import MyCallback, start_buttons, add_comment_to_discussion
from text_answers.answers import deal_add_ok, comment_add_ok, contact_add_error, deal_add_error, \
    comment_to_discus_add_error, company_add_error
from utils.states import Bitrix
from bot_data.info_for_bitrix import Info
from bitrix import bitrix_add_deal, bitrix_add_contact, bitrix_comment_to_discussion
from utils.update_deal_data import update_data

router = Router()


def print_deals():
    def return_deals(deals: list):
        show = 'И так, вот твои сделки:\n'
        for item in deals:
            show += f"Название сделки \- Сделка №`{item['deal_id']}`\_BOT\n"
            show += f"Имя клиента \- {item['name']}\n"
            show += f"Комментарий к сделке \- {item['comment']}\n\n"
        return show

    def take_info():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        info_path = os.path.join(current_dir, '..', 'bitrix', 'deal_information', 'deal_info.json')
        with open(info_path, 'r') as f:
            info = json.load(f)
            data = [{'name': item['name'], 'comment': item['comment'], 'deal_id': item['deal_id']} for item in info]
        return data

    result = return_deals(take_info())
    return result


@router.callback_query(MyCallback.filter(F.foo == 'show_deals'))
async def show_deals(query: CallbackQuery, bot: Bot, state: FSMContext):
    await query.message.answer('И так, вот все твои сделки')
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await query.message.answer(print_deals())