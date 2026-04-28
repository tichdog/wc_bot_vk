from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message
from filters.permition import IsPermission
from keyboards import get_keyboard
from utils import get_or_create_user

labeler = BotLabeler()


@labeler.message(IsPermission("Особое приветствие"), text=["начать", "Начать", "/start", "start"])
async def cmd_start(message: Message):
    user = get_or_create_user(message)

    await message.answer(
        "Добро пожаловать, администратор! Я готов к работе. "
        "Выберите пункт ниже, что бы Вы хотели сделать?",
        keyboard=get_keyboard(user),
    )


@labeler.message(text=["начать", "Начать", "/start", "start"])
async def cmd_start(message: Message):
    user = get_or_create_user(message)

    await message.answer(
        "Привет! Я — бот для сбора обратной связи о неполадках в помещениях.",
        keyboard=get_keyboard(user),
    )