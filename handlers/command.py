from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message
from filters.permition import IsPermission
from keyboards import get_keyboard
from utils import get_or_create_user

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [IsPermission("Приветствие администратора")]

user_labeler = BotLabeler()


@admin_labeler.message(text=["начать", "Начать", "/start", "start", "Привет", "привет"])
async def cmd_start(message: Message):
    user = get_or_create_user(message)

    await message.answer(
        "Добро пожаловать, администратор! Я готов к работе. "
        "Выберите пункт ниже, что бы Вы хотели сделать?",
        keyboard=get_keyboard(user),
    )


@user_labeler.message(text=["начать", "Начать", "/start", "start", "Привет", "привет"])
async def cmd_start(message: Message):
    user = get_or_create_user(message)

    await message.answer(
        "Привет! Я — бот для сбора обратной связи о неполадках в помещениях.",
        keyboard=get_keyboard(user),
    )