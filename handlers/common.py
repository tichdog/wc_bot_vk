from vkbottle.bot import Bot, Message
from keyboards import get_main_keyboard, get_admin_menu
from filters import IsRole

is_admin = IsRole("Администратор")


def register_common_handlers(bot: Bot):

    @bot.on.message()
    async def command_unknown(message: Message):

        state = await bot.state_dispenser.get(message.from_id)
        if state is not None:
            return

        if is_admin(message):
            await message.answer(
                "Не понимаю такую команду.",
                keyboard=get_admin_menu(),
            )
        else:
            await message.answer(
                "Не понимаю такую команду.\n"
                "Напиши 'Помощь', чтобы увидеть список доступных команд.",
                keyboard=get_main_keyboard(),
            )