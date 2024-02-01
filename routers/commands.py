from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import MyCallback, start_buttons
from utils.states import Bitrix
from bot_data.info_for_bitrix import info
from bitrix import bitrix_add_deal,bitrix_add_contact


router = Router()


# Вывод сообщения при старте
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}, что хочешь сделать??', reply_markup=start_buttons())


@router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Все этапы были отменены, можешь начинать сначала', reply_markup=start_buttons())


# Отрабатываем Stage's для получения информации для карточки
@router.callback_query(MyCallback.filter(F.foo == 'Bitrix24'))
async def start_bitrix(query: CallbackQuery, bot: Bot, state : FSMContext):
    await query.message.answer('Окей, заполним заказ и отправим в Битрикс')
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id) # удаляем кнопку
    await query.answer()
    await state.set_state(Bitrix.name)
    await query.message.answer('Для начала, введи имя')


@router.message(Bitrix.name)
async def bitrix_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    get_data = await state.get_data()
    info['name'] = get_data.get('name')
    await state.set_state(Bitrix.second_name)
    await message.answer('Теперь введи фамилию')


@router.message(Bitrix.second_name)
async def bitrix_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    get_data = await state.get_data()
    info['second_name'] = get_data.get('second_name')
    await state.set_state(Bitrix.city)
    await message.answer('Теперь введи город')


@router.message(Bitrix.city)
async def bitrix_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    get_data = await state.get_data()
    info['city'] = get_data.get('city')
    await state.set_state(Bitrix.job_title)
    await message.answer('Теперь введи должность')


@router.message(Bitrix.job_title)
async def bitrix_city(message: Message, state: FSMContext):
    await state.update_data(job_title=message.text)
    get_data = await state.get_data()
    info['job_title'] = get_data.get('job_title')
    await state.set_state(Bitrix.tenchat_link)
    await message.answer('Теперь введи ссылку на тенчат')


@router.message(Bitrix.tenchat_link)
async def bitrix_city(message: Message, state: FSMContext):
    await state.update_data(tenchat_link=message.text)
    get_data = await state.get_data()
    info['tenchat_link'] = get_data.get('tenchat_link')
    await state.set_state(Bitrix.comment)
    await message.answer('Теперь введи комментарий')


@router.message(Bitrix.comment)
async def bitrix_city(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    get_data = await state.get_data()
    info['comment'] = get_data.get('comment')
    await message.answer('Отлично, сейчас отправлю запрос и отпишусь')

    # Запускаем создание контакта
    contact = bitrix_add_contact.NewContact(info['name'], info['second_name'], info['city'], info['job_title'], info['tenchat_link'])
    respond_id = contact.send_request() # Получаем результат создания контакта
    if respond_id is None:
        await message.answer('⚠⚠⚠ООй-ой, что то пошло не так на этапе создания ➡контакта⬅, '
                             ' сообщи разработчику чтобы он проверил логи🔎🔎🔎, или попробуй еще раз',
                             reply_markup=start_buttons())
        return

    # Запускаем создание сделки
    deal = bitrix_add_deal.NewDeal(info['comment'], respond_id)
    final_respond = deal.send_request()
    if final_respond is not True:
        await message.answer('⚠⚠⚠Ой-ой, что то пошло не так на этапе создания ➡сделки⬅, '
                             'сообщи разработчику чтобы он проверил логи🔎🔎🔎, или попробуй еще раз',
                             reply_markup=start_buttons())
        return

    await message.answer('Всё прошло успешно👍👍, иди проверь сделку, '
                         'или можешь сразу создать еще одну👇👇👇', reply_markup=start_buttons())



