from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message

from keyboards import get_main_keyboard, get_admin_menu
from filters import IsRole

labeler = BotLabeler()
is_admin = IsRole("Администратор")


@labeler.message()
async def command_unknown(message: Message):
    if is_admin(message):
        await message.answer("Не понимаю такую команду.", keyboard=get_admin_menu())
    else:
        await message.answer(
            "Не понимаю такую команду.\n"
            "Напиши 'Помощь', чтобы увидеть список доступных команд.",
            keyboard=get_main_keyboard(),
        )