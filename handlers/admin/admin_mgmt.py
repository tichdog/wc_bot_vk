from vkbottle.bot import Bot, Message

from filters import IsRole
from keyboards import get_admin_menu
from models import User, Role, UserRole
from states import AdminStates

is_admin = IsRole("Администратор")


def register_admin_mgmt_handlers(bot: Bot):

    @bot.on.message(text=["Добавить администратора"])
    async def ask_admin_id(message: Message):
        if not is_admin(message):
            return

        await bot.state_dispenser.set(message.from_id, AdminStates.waiting_for_admin_id)
        await message.answer(
            "Введите VK ID пользователя, которого хотите назначить администратором.\n"
            "Отправьте /cancel, чтобы отменить."
        )


async def handle_waiting_for_admin_id(bot: Bot, message: Message):
    if message.text.strip().lower() in ("/cancel", "отмена"):
        await bot.state_dispenser.delete(message.from_id)
        await message.answer("Действие отменено.", keyboard=get_admin_menu())
        return

    raw = message.text.strip()
    if not raw.isdigit() or int(raw) < 9 or int(raw) > 10:
        await message.answer(
            "Некорректный ID. Введите числовой VK ID пользователя "
            "или /cancel для отмены."
        )
        return

    target_id = int(raw)

    if target_id == message.from_id:
        await message.answer(
            "Вы уже являетесь администратором\n"
            "Введите другой ID или /cancel."
        )
        return

    admin_role, _ = Role.get_or_create(name="Администратор")
    user, _ = User.get_or_create(id=target_id)

    already = UserRole.select().where(
        (UserRole.user == user) &
        (UserRole.role == admin_role)
    ).exists()

    if already:
        await bot.state_dispenser.delete(message.from_id)
        await message.answer(
            f"Пользователь с ID {target_id} уже является администратором.",
            keyboard=get_admin_menu(),
        )
        return

    UserRole.create(user=user, role=admin_role)

    await bot.state_dispenser.delete(message.from_id)
    await message.answer(
        f"Пользователь с ID {target_id} успешно назначен администратором.",
        keyboard=get_admin_menu(),
    )