import requests
import json
from datetime import datetime
from bitrix.urls import client_url, webhook_deal_add
import os


class NewDeal:
    """
    id - id клиента который получаем из bitrix_add_contact
    Получаем данные со счётчика, для названия карточки, отправляем данные на сайт, получаем ответ
    Если ответ 200 - прибавляем к счётчику +1 и возвращаем True
    Если получили ошибку - формируется json файл с url, данными и ошибкой и возвращает False
    """
    def __init__(self, comment: str, id: int,):
        self.comment = comment
        self.id = id
        self.url = f"https://{client_url}/rest/1/{webhook_deal_add}/crm.deal.add"

    def send_request(self):
        # Получаем путь к текущему файлу
        current_file_path = os.path.realpath(__file__)

        # Получаем путь к каталогу, в котором находится текущий файл
        current_directory = os.path.dirname(current_file_path)

        # Создаем путь к файлу 'counter.txt'
        counter_file_path = str(os.path.join(current_directory, 'counter.txt'))
        with open(counter_file_path, 'r+') as f:
            number = int(f.read())
        data = {
            "fields": {
                "COMMENTS": f"{self.comment}",
                "CONTACT_ID": f"{self.id}",
                "TITLE": f"Сделка №{number}_BOT",
            },
            "params": {
                "REGISTER_SONET_EVENT": "Y"
            }
        }
        response = requests.post(self.url, json=data)
        if response.status_code == 200:
            print("Создан контакт с ID " + str(response.json()))
            with open(counter_file_path, 'r+') as f:
                f.seek(0)
                f.write(str(number+1))
                f.truncate()
        else:
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"error_{now_str}.json"
            print("Ошибка: " + str(response.json()))
            error_data = {
                "url": self.url,
                "data": data,
                "error": response.json()
            }
            with open(filename, 'w') as f:
                json.dump(error_data, f)
        return True if response.status_code == 200 else False


if __name__ == '__main__':
    # тест
    gg = NewDeal('Коммент сделки','15')
    gg.send_request()





