from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import ABCRule
from typing import Optional, Dict, Any

from models import Room, User, UserRole, Role
from keyboards import get_admin_menu
from states import AdminStates
from dispenser import state_dispenser

labeler_room = BotLabeler()

class IsAdminRule(ABCRule[Message]):
    async def check(self, message: Message) -> Optional[Dict[str, Any]]:
        user = User.get_or_none(id=message.from_id)
        if not user:
            return False

        admin_role = Role.get_or_none(name="Администратор")
        if not admin_role:
            return False

        user_role = UserRole.get_or_none(user=user, role=admin_role)
        if user_role:
            return {"is_admin": True, "user_id": message.from_id}
        return False


labeler_room.auto_rules = [IsAdminRule()]


@labeler_room.message(text=["Добавить помещение", "Добавить", "/add", "/add_room"])
async def add_room_start(message: Message):
    await state_dispenser.set(message.peer_id, AdminStates.waiting_for_room_name)
    await message.answer("Введите название помещения:")


@labeler_room.message(text="Список помещений")
async def list_rooms(message: Message):
    rooms = Room.get_active_by_user(message.from_id)

    if not rooms:
        await message.answer("Нет доступных помещений", keyboard=get_admin_menu())
        return

    text = "\n".join(f"• {room.name}" for room in rooms)
    await message.answer(f"Список помещений:\n\n{text}", keyboard=get_admin_menu())


@labeler_room.message(state=AdminStates.waiting_for_room_name)
async def handle_waiting_for_room_name(message: Message):
    room_name = message.text.strip()

    if not room_name:
        await message.answer("Название не может быть пустым. Попробуйте ещё раз:")
        return

    existing_rooms = Room.get_active_by_user(message.from_id)
    if any(room.name == room_name for room in existing_rooms):
        await message.answer("Помещение с таким названием уже существует. Попробуйте другое:")
        return

    user, _ = User.get_or_create(id=message.from_id)
    Room.create(name=room_name, creator=user)

    await state_dispenser.delete(message.peer_id)
    await message.answer(f"Помещение '{room_name}' добавлено!", keyboard=get_admin_menu())