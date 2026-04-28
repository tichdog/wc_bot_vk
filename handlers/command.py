from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message
from filters.permition import IsPermission
from keyboards import get_keyboard

labeler = BotLabeler()


@labeler.message(IsPermission("Особое приветствие"), text=["начать", "Начать", "/start", "start"])
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать, администратор! Я готов к работе. "
        "Выберите пункт ниже, что бы Вы хотели сделать?",
        keyboard=get_keyboard(message),
    )


@labeler.message(text=["начать", "Начать", "/start", "start"])
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я — бот для сбора обратной связи о неполадках в помещениях.",
        keyboard=get_keyboard(message),
    )