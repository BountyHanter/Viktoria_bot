import requests
import json
from datetime import datetime
from bitrix.urls import client_url, webhook_contact_add


class NewCompany:
    """
    Класс создаёт новый контакт
    client_url - адрес сайта клиента
    webhook_contact_add - адрес вебхука действия

    send_request - Отправляет запрос на адрес, и получает ответ, если ответ - 200, берёт ид контакта из результата
    и возвращает его, если произошла ошибка то формируется json файл с url, данными и ошибкой и возвращает None

    """
    def __init__(self, name: str,):
        self.url = f"https://{client_url}/rest/13/{webhook_contact_add}/crm.company.add"
        self.data = {
            "fields": {
                "TITLE": f"{name}",
            },
            "params": {
                "REGISTER_SONET_EVENT": "Y"
            }
        }

    def send_request(self):
        response = requests.post(self.url, json=self.data)
        if response.status_code == 200:
            print("Создана компания с ID " + str(response.json()))
            # Получаем данные из ответа
            data = response.json()
            data_id = int(data['result'])
        else:
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"error_{now_str}.json"
            print("Ошибка: " + str(response.json()))
            error_data = {
                "url": self.url,
                "data": self.data,
                "error": response.json()
            }
            with open(filename, 'w') as f:
                json.dump(error_data, f)
        return data_id if response.status_code == 200 else None


if __name__ == "__main__":
    # Тест
    gg = NewCompany('АО "МММ"')
    gg.send_request()



