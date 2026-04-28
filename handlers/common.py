from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message
from keyboards import get_keyboard
from filters.permition import IsPermission
from utils import get_or_create_user

labeler = BotLabeler()


@labeler.message(IsPermission("Управление ботом"))
async def command_unknown(message: Message):
    user = get_or_create_user(message)
    await message.answer("Не понимаю такую команду.", keyboard=get_keyboard(user))


@labeler.message()
async def command_unknown(message: Message):
    user = get_or_create_user(message)
    await message.answer(
        "Не понимаю такую команду.\n"
        "Напиши 'Помощь', чтобы увидеть список доступных команд.",
        keyboard=get_keyboard(user),
    )