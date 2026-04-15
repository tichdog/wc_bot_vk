from vkbottle.bot import Bot, Message

from filters import IsRole
from keyboards import get_admin_menu
from models import User


is_admin = IsRole("Администратор")

def register_admin_command_handlers(bot: Bot):
    @bot.on.message(text=["начать", "Начать", "/start", "start"])
    async def cmd_start(message: Message):
        User.get_or_create(id=message.from_id)

        if not is_admin(message):
            await message.answer(
                "Привет! Я — бот для сбора обратной связи о неполадках в помещениях."
            )
            return

        await message.answer(
            "Добро пожаловать, администратор! Я готов к работе. "
            "Выберите пункт ниже, что бы Вы хотели сделать?",
            keyboard=get_admin_menu(),
        )
