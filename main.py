import os
from dotenv import load_dotenv
from vkbottle.bot import Bot
from handlers import register_all_handlers

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
register_all_handlers(bot)

if __name__ == "__main__":
    print("Бот запущен")
    bot.run_forever()