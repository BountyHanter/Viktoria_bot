from aiogram.fsm.state import StatesGroup, State


# Stage для создания сделки в Bitrix
class Bitrix(StatesGroup):
    name = State()
    second_name = State()
    city = State()
    job_title = State()
    tenchat_link = State()
    company_name = State()
    comment = State()
    comment_to_discus = State()
    info = State()  # переменная чтобы хранить экземпляр класса информации о сделке для последующего его перенаса в кэш
    id_number = State()
