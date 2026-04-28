from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message

from filters.permition import IsPermission
from keyboards import get_keyboard
from models import Room, User
from states import AdminStates
from dispenser import state_dispenser
from utils import get_or_create_user

labeler = BotLabeler()


@labeler.message(IsPermission("Добавить помещение"), text=["Добавить помещение", "/add"])
async def add_room_start(message: Message):
    await state_dispenser.set(message.from_id, AdminStates.waiting_for_room_name)
    await message.answer("Введите название помещения:")


@labeler.message(IsPermission("Список помещений"), text="Список помещений")
async def list_rooms(message: Message):
    user_db = get_or_create_user(message)
    rooms = Room.get_active_by_user(message.from_id)
    if not rooms:
        await message.answer("Нет доступных помещений", keyboard=get_keyboard(user_db))
        return
    text = "\n".join(f"• {room.name}" for room in rooms)
    await message.answer(f"Список помещений:\n\n{text}", keyboard=get_keyboard(user_db))


@labeler.message(IsPermission("Добавить помещение"), state=AdminStates.waiting_for_room_name)
async def handle_waiting_for_room_name(message: Message):
    user_db = get_or_create_user(message)
    room_name = message.text.strip()
    if not room_name:
        await message.answer("Название не может быть пустым. Попробуйте ещё раз:")
        return
    user, _ = User.get_or_create(id=message.from_id)
    Room.create(name=room_name, creator=user)
    await state_dispenser.delete(message.from_id)
    await message.answer(f"Помещение '{room_name}' добавлено!", keyboard=get_keyboard(user_db))