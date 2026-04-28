from vkbottle import Keyboard, Text, KeyboardButtonColor
from models import User, Role, UserRole


def kb_main():
    return [
        [("Привет", KeyboardButtonColor.POSITIVE),
         ("ID", KeyboardButtonColor.PRIMARY),
         ("Помощь", KeyboardButtonColor.SECONDARY)]
    ]

def kb_manager():
    return [
        [("Добавить помещение", KeyboardButtonColor.POSITIVE),
         ("Список помещений", KeyboardButtonColor.PRIMARY)]
    ]

def kb_admin():
    return [
        [("Добавить администратора", KeyboardButtonColor.POSITIVE),
            ("Добавить менеджера", KeyboardButtonColor.POSITIVE),]
    ]

def has_role(user: User, role_name: str) -> bool:
    return UserRole.get_or_none(
        (UserRole.user == user) &
        (UserRole.role == Role.get(name=role_name))
    ) is not None

def get_keyboard(user: User) -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=False)
    rows = []
    rows += kb_main()

    if has_role(user, "Менеджер"):
        rows += kb_manager()

    if has_role(user, "Администратор"):
        rows += kb_manager()
        rows += kb_admin()

    for row in rows:
        for text, color in row:
            keyboard.add(Text(text), color=color)
        keyboard.row()

    return keyboard