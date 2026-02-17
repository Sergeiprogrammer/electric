import time
import requests
from bs4 import BeautifulSoup
import json

def get_info(argument):
    all_info1 = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for j in range(argument):
        url = f'https://elektrodistribucija.rs/planirana-iskljucenja-srbija/Nis_Dan_{j}_Iskljucenja.htm'
        # Отправляем HTTP-запрос к странице с заголовками
        response = requests.get(url, headers=headers)

        # Проверяем, что запрос успешен
        if response.status_code == 200:
            # Создаем объект BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            value = 0
            all_info = []
            # Находим все теги <tr> с атрибутом bgcolor="#DDDDDD"
            for i in soup.find_all('table')[1].findAll('td'):
                if "Црвени крст" in i.text or "делничка" in i.text:
                    value = 3
                if value != 0:
                    all_info.append(i.text.strip())  # Удаляем лишние пробелы и символы
                    value -= 1
            all_info.append(f"через {j} от сегодня")
        else:
            return response.status_code

        if len(all_info) > 1:
            all_info1.append(all_info)
        else:
            pass

    # Преобразуем all_info1 в строковый формат для записи в файл
    all_info1_str = "\n".join([", ".join(info) for info in all_info1])

    # Читаем содержимое файла
    try:
        with open("output.txt", "r") as file:
            file_content = file.read().strip()  # Удаляем пробелы и переносы строк для корректного сравнения
    except FileNotFoundError:
        file_content = ""  # Если файла нет, то сравнивать не с чем

    # Сравниваем содержимое файла с новым all_info1
    if all_info1_str != file_content:
        # Если не совпадает, записываем новые данные в файл
        with open("output.txt", "w") as file:
            file.write(all_info1_str)
        return all_info1  # Возвращаем all_info1, если данные изменились
    else:
        return False  # Если данные совпадают, возвращаем False

def check_dict(arg):
    date_dict = {
        "через 0 от сегодня": "сегодня",
        "через 1 от сегодня": "завтра",
        "через 2 от сегодня": "послезавтра"
    }
    try:
        return date_dict.get(arg, None)
    except:
        return Exception
