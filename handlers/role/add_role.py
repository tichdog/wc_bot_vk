from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.bot import BotLabeler, Message, rules
from filters.permition import IsPermission
from keyboards import get_keyboard
from models import User, Role, UserRole
from states import AdminStates
from dispenser import state_dispenser
from utils import get_or_create_user


labeler = BotLabeler()
labeler.auto_rules = [IsPermission("Добавить администратора")]


@labeler.message(text=["Добавить администратора"])
async def ask_admin_id(message: Message):
    await state_dispenser.set(message.from_id, AdminStates.waiting_for_admin_id)
    await message.answer(
        "Введите VK ID пользователя, которого хотите назначить администратором.\n"
        "Отправьте /cancel, чтобы отменить."
    )


@labeler.message(state=AdminStates.waiting_for_admin_id)
async def handle_waiting_for_admin_id(message: Message):
    user_db = get_or_create_user(message)
    if message.text.strip().lower() in ("/cancel", "отмена"):
        await state_dispenser.delete(message.from_id)
        await message.answer("Действие отменено.", keyboard=get_keyboard(user_db))
        return

    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer(
            "Некорректный ID. Введите числовой VK ID пользователя "
            "или /cancel для отмены."
        )
        return

    if not (9 <= len(raw) <= 11):
        await message.answer("Некорректный ID, неверное количество цифр.")
        return

    target_id = int(raw)
    if target_id == message.from_id:
        await message.answer("Вы уже являетесь администратором.\nВведите другой ID или /cancel.")
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
            keyboard=get_keyboard(user_db),
        )
        return

    UserRole.create(user=user, role=admin_role)
    await state_dispenser.delete(message.from_id)
    await message.answer(
        f"Пользователь с ID {target_id} успешно назначен администратором.",
        keyboard=get_keyboard(user_db),
    )

@labeler.message(text=["Добавить менеджера"])
async def ask_manager_id(message: Message):
    await state_dispenser.set(message.from_id, AdminStates.waiting_for_manager_id)
    await message.answer(
        "Введите VK ID пользователя, которого хотите назначить менеджером.\n"
        "Отправьте /cancel, чтобы отменить."
    )


@labeler.message(state=AdminStates.waiting_for_manager_id)
async def handle_waiting_for_manager_id(message: Message):
    user_db = get_or_create_user(message)
    if message.text.strip().lower() in ("/cancel", "отмена"):
        await state_dispenser.delete(message.from_id)
        await message.answer("Действие отменено.", keyboard=get_keyboard(user_db))
        return

    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer(
            "Некорректный ID. Введите числовой VK ID или /cancel для отмены."
        )
        return

    if not (9 <= len(raw) <= 11):
        await message.answer("Некорректный ID, неверное количество цифр.")
        return

    target_id = int(raw)
    manager_role, _ = Role.get_or_create(name="Менеджер")
    user, _ = User.get_or_create(id=target_id)

    already = UserRole.select().where(
        (UserRole.user == user) & (UserRole.role == manager_role)
    ).exists()

    if already:
        await state_dispenser.delete(message.from_id)
        await message.answer(
            f"Пользователь с ID {target_id} уже является менеджером.",
            keyboard=get_keyboard(user_db),
        )
        return

    UserRole.create(user=user, role=manager_role)
    await state_dispenser.delete(message.from_id)
    await message.answer(
        f"Пользователь с ID {target_id} успешно назначен менеджером.",
        keyboard=get_keyboard(user_db),
    )