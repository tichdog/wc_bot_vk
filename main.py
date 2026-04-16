import os
from dotenv import load_dotenv
from vkbottle.bot import Bot
from handlers import register_all_handlers
from dispenser import state_dispenser
from models import create_tables, db

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN, state_dispenser=state_dispenser)
register_all_handlers(bot)

if __name__ == "__main__":
    create_tables()
    db.connect(reuse_if_open=True)
    print("Бот запущен")
    bot.run_forever()