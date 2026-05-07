from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message

from filters.permition import IsPermission
from keyboards import get_keyboard
from models import Room
from utils import get_or_create_user

labeler = BotLabeler()


@labeler.message(IsPermission("Список помещений"), text="Список помещений")
async def list_rooms(message: Message):
    user_db = get_or_create_user(message)
    rooms = Room.get_active_by_user(message.from_id)
    if not rooms:
        await message.answer("Нет доступных помещений", keyboard=get_keyboard(user_db))
        return
    text = "\n".join(f"• {room.name}" for room in rooms)
    await message.answer(f"Список помещений:\n\n{text}", keyboard=get_keyboard(user_db))