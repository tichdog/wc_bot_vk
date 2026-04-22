from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import Message

from filters import IsRole
from keyboards import get_admin_menu
from models import User, Role, UserRole
from states import AdminStates
from dispenser import state_dispenser

labeler = BotLabeler()
is_admin = IsRole("Администратор")


@labeler.message(text=["Добавить администратора"])
async def ask_admin_id(message: Message):
    if not is_admin(message):
        return
    await state_dispenser.set(message.from_id, AdminStates.waiting_for_admin_id)
    await message.answer(
        "Введите VK ID пользователя, которого хотите назначить администратором.\n"
        "Отправьте /cancel, чтобы отменить."
    )


@labeler.message(state=AdminStates.waiting_for_admin_id)
async def handle_waiting_for_admin_id(message: Message):
    if message.text.strip().lower() in ("/cancel", "отмена"):
        await state_dispenser.delete(message.from_id)
        await message.answer("Действие отменено.", keyboard=get_admin_menu())
        return

    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer(
            "Некорректный ID. Введите числовой VK ID пользователя "
            "или /cancel для отмены."
        )
        return

    if len(raw) < 9 or len(raw) > 11:
        await message.answer(
            "Некорректный ID, неверное количество чисел."
        )
        return

    target_id = int(raw)
    if target_id == message.from_id:
        await message.answer("Вы уже являетесь администратором\nВведите другой ID или /cancel.")
        return

    admin_role, _ = Role.get_or_create(name="Администратор")
    user, _ = User.get_or_create(id=target_id)
    already = UserRole.select().where(
        (UserRole.user == user) & (UserRole.role == admin_role)
    ).exists()

    if already:
        await state_dispenser.delete(message.from_id)
        await message.answer(
            f"Пользователь с ID {target_id} уже является администратором.",
            keyboard=get_admin_menu(),
        )
        return

    UserRole.create(user=user, role=admin_role)
    await state_dispenser.delete(message.from_id)
    await message.answer(
        f"Пользователь с ID {target_id} успешно назначен администратором.",
        keyboard=get_admin_menu(),
    )