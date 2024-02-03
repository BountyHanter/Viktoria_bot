from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.inline import start_buttons

router = Router()


# Вывод сообщения при старте
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}, что хочешь сделать??', reply_markup=start_buttons())


@router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Все этапы были отменены, можешь начинать сначала', reply_markup=start_buttons())
