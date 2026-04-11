from vkbottle.bot import Bot, Message
from keyboards import get_main_keyboard


def register_common_handlers(bot: Bot):

    @bot.on.message()
    async def command_unknown(message: Message):
        await message.answer(
            "Не понимаю такую команду.\n"
            "Напиши 'Помощь', чтобы увидеть список доступных команд.",
            keyboard=get_main_keyboard(),
        )