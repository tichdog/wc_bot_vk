import os
from dotenv import load_dotenv
from vkbottle.bot import Bot, BotLabeler
from handlers import register_all_handlers
from dispenser import state_dispenser
from models import create_tables, db
from handlers.admin.room import labeler
from states import AdminStates

main_labeler = BotLabeler()
main_labeler.load(labeler)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN, state_dispenser=state_dispenser)
bot.labeler = main_labeler

register_all_handlers(bot)

if __name__ == "__main__":
    create_tables()
    db.connect(reuse_if_open=True)
    print("Бот запущен")
    bot.run_forever()