# Загрузка данных в кэш
import json
import os

from aiogram.fsm.context import FSMContext

current_dir = os.path.dirname(os.path.abspath(__file__))


async def update_data(state: FSMContext):
    info_path = os.path.join(current_dir, '..', 'bitrix', 'deal_information', 'deal_info.json') # получаем путь к json
    get_data = await state.get_data()
    info = get_data.get('info')
    info_dict = info.to_dict()

    with open(info_path, 'r+') as f:
        if f.read().strip():  # проверяем, что файл не пуст
            f.seek(0)  # возвращаем указатель в начало файла
            data = json.load(f)
        else:
            data = []  # инициализируем пустой список, если файл пуст

        data.append(info_dict)  # добавляем новый словарь в список

        f.seek(0)
        json.dump(data, f, ensure_ascii=False)
        f.truncate()