from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message

from dispenser import state_dispenser
from keyboards import get_main_keyboard, get_admin_menu
from filters import IsRole
from states import AdminStates
from handlers.admin.room import handle_waiting_for_room_name
from handlers.admin.admin_mgmt import handle_waiting_for_admin_id

labeler = BotLabeler()
is_admin = IsRole("Администратор")


@labeler.message()
async def command_unknown(message: Message):
    state = await state_dispenser.get(message.from_id)

    if state is not None:
        if state.state == AdminStates.waiting_for_room_name:
            await handle_waiting_for_room_name(message)
        elif state.state == AdminStates.waiting_for_admin_id:
            await handle_waiting_for_admin_id(message)
        return

    if is_admin(message):
        await message.answer("Не понимаю такую команду.", keyboard=get_admin_menu())
    else:
        await message.answer(
            "Не понимаю такую команду.\n"
            "Напиши 'Помощь', чтобы увидеть список доступных команд.",
            keyboard=get_main_keyboard(),
        )