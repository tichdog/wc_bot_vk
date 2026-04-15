from vkbottle.bot import Bot, Message

from filters import IsRole
from keyboards import get_admin_menu
from models import Room, User
from states import AdminStates

is_admin = IsRole("Администратор")


def register_admin_room_handlers(bot: Bot):

    @bot.on.message(text=["Добавить помещение", "Добавить", "/add", "/add_room"])
    async def add_room_start(message: Message):
        if not is_admin(message):
            return

        await bot.state_dispenser.set(message.from_id, AdminStates.waiting_for_room_name)
        await message.answer("Введите название помещения:")

    @bot.on.message(text="Список помещений")
    async def list_rooms(message: Message):
        if not is_admin(message):
            return

        rooms = Room.get_active_by_user(message.from_id)

        if not rooms:
            await message.answer("Нет доступных помещений", keyboard=get_admin_menu())
            return

        text = "\n".join(f"• {room.name}" for room in rooms)
        await message.answer(f"Список помещений:\n\n{text}", keyboard=get_admin_menu())


async def handle_waiting_for_room_name(bot: Bot, message: Message):
    room_name = message.text.strip()

    if not room_name:
        await message.answer("Название не может быть пустым. Попробуйте ещё раз:")
        return

    user, _ = User.get_or_create(id=message.from_id)
    Room.create(name=room_name, creator=user)

    await bot.state_dispenser.delete(message.from_id)
    await message.answer(
        f"Помещение '{room_name}' добавлено!",
        keyboard=get_admin_menu(),
    )