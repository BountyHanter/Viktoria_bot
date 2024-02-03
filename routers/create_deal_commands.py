from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import bitrix_add_company
from keyboards.inline import MyCallback, start_buttons, add_comment_to_discussion
from text_answers.answers import deal_add_ok, comment_add_ok, contact_add_error, deal_add_error, \
    comment_to_discus_add_error, company_add_error
from utils.states import Bitrix
from bot_data.info_for_bitrix import Info
from bitrix import bitrix_add_deal, bitrix_add_contact, bitrix_comment_to_discussion
from utils.update_deal_data import update_data

router = Router()


# Отрабатываем Stage's для получения информации для карточки
@router.callback_query(MyCallback.filter(F.foo == 'Bitrix24'))
async def start_bitrix(query: CallbackQuery, bot: Bot, state: FSMContext):
    info = Info()
    await state.update_data(info=info) # Переносим экземпляр в машину состояний
    await query.message.answer('Окей, заполним заказ и отправим в Битрикс')
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await state.set_state(Bitrix.name)
    await query.message.answer('Для начала, введи имя')


@router.message(Bitrix.name)
async def bitrix_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.name = get_data.get('name')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.second_name)
    await message.answer('Теперь введи фамилию')


@router.message(Bitrix.second_name)
async def bitrix_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.second_name = get_data.get('second_name')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.company_name)
    await message.answer('Теперь введи название компании')


@router.message(Bitrix.company_name)
async def bitrix_second_name(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.company_name = get_data.get('company_name')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.city)
    await message.answer('Теперь введи город')


@router.message(Bitrix.city)
async def bitrix_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.city = get_data.get('city')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.job_title)
    await message.answer('Теперь введи должность')


@router.message(Bitrix.job_title)
async def bitrix_job_title(message: Message, state: FSMContext):
    await state.update_data(job_title=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.job_title = get_data.get('job_title')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.tenchat_link)
    await message.answer('Теперь введи ссылку на тенчат')


@router.message(Bitrix.tenchat_link)
async def bitrix_tenchat_link(message: Message, state: FSMContext):
    await state.update_data(tenchat_link=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.tenchat_link = get_data.get('tenchat_link')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.comment)
    await message.answer('Теперь введи комментарий')


@router.message(Bitrix.comment)
async def bitrix_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.comment = get_data.get('comment')
    await state.update_data(info=info)  # обновляем info в state
    await message.answer('Отлично, сейчас отправлю запрос и отпишусь')

    # Запускаем создание контакта
    contact = bitrix_add_contact.NewContact(info.name, info.second_name,
                                            info.city, info.job_title,
                                            info.tenchat_link)
    respond_contact_id = contact.send_request()  # Получаем результат создания контакта
    if respond_contact_id is None:
        # Ошибка при создании контакта
        await message.answer(contact_add_error, reply_markup=start_buttons())
        return

    # Запускаем создание компании
    company = bitrix_add_company.NewCompany(info.company_name)
    respond_company = company.send_request()
    if respond_company is None:
        # Ошибка при создании контакта
        await message.answer(company_add_error, reply_markup=start_buttons())
        return

    # Запускаем создание сделки
    deal = bitrix_add_deal.NewDeal(info.comment, respond_contact_id, respond_company)
    final_respond = deal.send_request()  # Возвращается 2 элемента [айди сделки в битрикс, номер сделки]
    if final_respond[0] is False:
        # Ошибка при создании сделки
        await message.answer(deal_add_error, reply_markup=start_buttons())
        return
    print(info)
    info.deal_id = final_respond[0]
    info.id_number = final_respond[1]
    await state.update_data(info=info)  # обновляем info в state
    await message.answer(deal_add_ok, reply_markup=add_comment_to_discussion())


# Добавляем комментарий
@router.callback_query(MyCallback.filter(F.foo == 'add_comment_to_dicscussion'))
async def add_comment_to_discus(query: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await state.set_state(Bitrix.comment_to_discus)
    await query.message.answer('Хорошо, напиши свой комментарий и я добавлю его в обсуждение к сделке')


# Функция добавления комментария
@router.message(Bitrix.comment_to_discus)
async def comment_to_discussion(message: Message, state: FSMContext):
    await state.update_data(comment_to_discus=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.comment_to_discus = get_data.get('comment_to_discus')
    await state.update_data(info=info)  # обновляем info в state
    comment_to_discus = bitrix_comment_to_discussion.AddComment(info.comment_to_discus, info.deal_id)
    comment_to_discus.send_request()
    if comment_to_discus is False:
        # Ошибка при создании комментария к обсуждению
        await message.answer(comment_to_discus_add_error, reply_markup=start_buttons())
        return
    # await update_data(state)  # Загружаем данные сделки в кэш
    await message.answer(comment_add_ok, reply_markup=start_buttons())


# Не добавляем комментарий
@router.callback_query(MyCallback.filter(F.foo == 'not_add_comment_to_dicscussion'))
async def not_comment(query: CallbackQuery, bot: Bot, state: FSMContext):
    # await update_data(state)  # Загружаем данные сделки в кэш
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await query.message.answer('Хорошо, что нибудь еще?', reply_markup=start_buttons())
