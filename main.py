import os
from dotenv import load_dotenv

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor

load_dotenv()
TOKEN =  os.getenv("TOKEN")
bot = Bot(token=TOKEN)

def get_main_keyboard() -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("Привет"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("ID"),     color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Помощь"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

@bot.on.message(text=["привет", "Привет", "hi", "hello"])
async def cmd_hello(message: Message):
    user = await bot.api.users.get(user_ids=message.from_id)
    name = user[0].first_name if user else "друг"
    await message.answer(
        f"Привет, {name}!",
        keyboard=get_main_keyboard(),
    )

@bot.on.message(text=["id", "ID", "мой id", "Мой ID", "Id"])
async def cmd_id(message: Message):
    await message.answer(
        f"Твой VK ID: {message.from_id}",
        keyboard=get_main_keyboard(),
    )

@bot.on.message(text=["помощь", "Помощь", "help", "/help", "хелп"])
async def cmd_help(message: Message):
    help_text = (
        "Список команд:\n\n"
        "Привет — поздороваться с ботом\n"
        "ID     — узнать свой VK ID\n"
        "Помощь — показать это сообщение"
    )
    await message.answer(help_text, keyboard=get_main_keyboard())

@bot.on.message()
async def command_unknown(message: Message):
    await message.answer(
        "Не понимаю такую команду.\n"
        "Напиши «Помощь», чтобы увидеть список доступных команд.",
        keyboard=get_main_keyboard(),
    )

if __name__ == "__main__":
    print("Бот запущен!")
    bot.run_forever()