from vkbottle.bot import Bot, Message
from filters import IsRole
from keyboards import get_main_keyboard, get_admin_menu


is_admin = IsRole("Администратор")


def _keyboard_for(message: Message):
    return get_admin_menu() if is_admin(message) else get_main_keyboard()


def register_user_handlers(bot: Bot):

    @bot.on.message(text=["привет", "Привет", "hi", "hello"])
    async def cmd_hello(message: Message):
        user = await bot.api.users.get(user_ids=message.from_id)
        name = user[0].first_name if user else "друг"
        await message.answer(f"Привет, {name}!", keyboard=_keyboard_for(message))

    @bot.on.message(text=["id", "ID", "мой id", "Мой ID", "Id"])
    async def cmd_id(message: Message):
        await message.answer(f"Твой VK ID: {message.from_id}", keyboard=_keyboard_for(message))

    @bot.on.message(text=["помощь", "Помощь", "help", "/help", "хелп"])
    async def cmd_help(message: Message):
        help_text = (
            "Список команд:\n\n"
            "Привет — поздороваться с ботом\n"
            "ID     — узнать свой VK ID\n"
            "Помощь — показать это сообщение"
        )
        await message.answer(help_text, keyboard=_keyboard_for(message))