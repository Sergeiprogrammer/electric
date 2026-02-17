import time
from datetime import datetime
import threading
import telebot
from main import get_info, check_dict
import sys
bot = telebot.TeleBot('6986591700:AAF09IXA7OintoNq04QdnmQwoX3-LlaazZs')

# Обработчик команды /test
@bot.message_handler(commands=['test'])
def handle_test(message):
    bot.reply_to(message, "бот работает")


# Обработчик команды /shut_down
@bot.message_handler(commands=['shut_down'])
def initiate_shutdown(message):
    bot.reply_to(message, "выключение")
    bot.send_message(message.chat.id, "почему вы его выключаете?")
    bot.register_next_step_handler(message, confirm_shutdown)


def confirm_shutdown(message):
    try:
        # Проверяем наличие username у пользователя
        username = message.from_user.username if message.from_user.username else "Неизвестный пользователь"

        with open("bag_info.txt", "w", encoding='utf-8') as file:
            # Записываем username и текущую дату и время в файл
            file.write(f"Пользователь: {username}\n")
            file.write(f"причина: {message.text}\n")
            file.write(datetime.now().strftime("дата: %d.%m  время %H:%M"))

        # Отправляем подтверждающее сообщение
        bot.send_message(message.chat.id, "Запрос на выключение получен. Бот выключается.")

        # Останавливаем polling
        bot.stop_polling()

        # Завершаем выполнение программы
        sys.exit()

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


def start(message_id=-1002198826916):
    all_info = get_info(3)
    print(all_info)
    if all_info:
        for info_list in all_info[0]:
            result = check_dict(info_list)
            if result is None:
                bot.send_message(message_id, info_list)
            else:
                bot.send_message(message_id, result)
    if datetime.today().day == 30:
        bot.send_message(message_id, "Бот работает!")


def periodic_start():
    while True:
        start()
        time.sleep(4 * 3600)  # Задержка на 4 часа


# Запуск функции periodic_start в отдельном потоке
threading.Thread(target=periodic_start, daemon=True).start()

# Запуск бота для обработки команд
try:
    bot.polling(none_stop=True)
except KeyboardInterrupt:
    print("Бот остановлен вручную.")
except Exception as e:
    print(f"Произошла ошибка: {e}")


