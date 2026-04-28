from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message

from filters.permition import IsPermission
from keyboards import get_keyboard

labeler = BotLabeler()
is_admin = IsPermission("Управление ботом")


@labeler.message(text=["привет", "Привет", "hi", "hello"])
async def cmd_hello(message: Message):
    user = await message.ctx_api.users.get(user_ids=message.from_id)
    name = user[0].first_name if user else "друг"
    await message.answer(f"Привет, {name}!", keyboard=get_keyboard(message))


@labeler.message(text=["id", "ID", "мой id", "Мой ID", "Id"])
async def cmd_id(message: Message):
    await message.answer(f"Твой VK ID: {message.from_id}", keyboard=get_keyboard(message))


@labeler.message(text=["помощь", "Помощь", "help", "/help", "хелп"])
async def cmd_help(message: Message):
    help_text = (
        "Список команд:\n\n"
        "Привет — поздороваться с ботом\n"
        "ID     — узнать свой VK ID\n"
        "Помощь — показать это сообщение"
    )
    await message.answer(help_text, keyboard=get_keyboard(message))