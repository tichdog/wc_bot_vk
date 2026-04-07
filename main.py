import os
import random
from datetime import datetime

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('VK_TOKEN')

def send_message(vk, user_id, message):
    """Отправка сообщения пользователю"""
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0
    )

def main():
    if not TOKEN:
        print("Токен не найден в файле .env")
        return

    # Авторизация бота
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("Бот запущен")

    # Цикл обработки сообщений
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = get_user_id(event)
            message = event.text.lower().strip()
            # Обработка команд
            if message == 'привет':
                send_message(vk, user_id, "Привет!")
            elif message == 'id':
                send_message(vk, user_id, f"ID: {user_id}")
            else:
                send_message(vk, user_id, "Не понимаю команду")


def get_user_id(event):
    return event.user_id

def add_admin_by_id(msg):
    return 0

if __name__ == '__main__':
    main()