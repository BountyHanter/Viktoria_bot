from aiogram.fsm.state import StatesGroup, State

# Stage для создания сделки в Bitrix
class Bitrix(StatesGroup):
    name = State()
    second_name = State()
    city = State()
    job_title = State()
    tenchat_link = State()
    comment = State()