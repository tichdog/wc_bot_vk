from vkbottle.bot import Bot, Message

from handlers.admin.room import handle_waiting_for_room_name
from handlers.admin.admin_mgmt import handle_waiting_for_admin_id
from states import AdminStates


def register_admin_state_handlers(bot: Bot):

    @bot.on.message()
    async def handle_admin_states(message: Message):
        state = await bot.state_dispenser.get(message.from_id)
        if state is None:
            return

        if state.state == AdminStates.waiting_for_room_name:
            await handle_waiting_for_room_name(bot, message)

        elif state.state == AdminStates.waiting_for_admin_id:
            await handle_waiting_for_admin_id(bot, message)