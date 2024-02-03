import requests
import json
from datetime import datetime
from bitrix.urls import client_url, webhook_contact_add


class NewContact:
    """
    Класс создаёт новый контакт
    client_url - адрес сайта клиента
    webhook_contact_add - адрес вебхука действия

    send_request - Отправляет запрос на адрес, и получает ответ, если ответ - 200, берёт ид контакта из результата
    и возвращает его, если произошла ошибка то формируется json файл с url, данными и ошибкой и возвращает None

    """
    def __init__(self, name: str,
                 second_name: str,
                 city: str,
                 job_title: str,
                 tenchat_link: str,):
        self.url = f"https://{client_url}/rest/13/{webhook_contact_add}/crm.contact.add"
        self.data = {
            "fields": {
                "ADDRESS_CITY": f"{city}",
                "LAST_NAME": f"{second_name}",
                "NAME": f"{name}",
                "POST": f"{job_title}",
                "UF_CRM_1706861554878": f"{tenchat_link}"
            },
            "params": {
                "REGISTER_SONET_EVENT": "Y"
            }
        }

    def send_request(self):
        response = requests.post(self.url, json=self.data)
        if response.status_code == 200:
            print("Создан контакт с ID " + str(response.json()))
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
    gg = NewContact('Александр2','Шляпик1', 'Город', 'Шестёрка', 'https://tenchat.ru/angelina_arttt')
    gg.send_request()



