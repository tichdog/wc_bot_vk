from vkbottle import Keyboard, Text, KeyboardButtonColor
from filters.permition import IsPermission
from vkbottle.bot import Message

def get_main_keyboard() -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("Привет"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("ID"),     color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Помощь"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_manager_keyboard() -> Keyboard:
    keyboard = get_main_keyboard()
    keyboard.row()
    keyboard.add(Text("Добавить помещение"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Список помещений"), color=KeyboardButtonColor.PRIMARY)
    return keyboard

def get_admin_keyboard() -> Keyboard:
    keyboard = get_manager_keyboard()
    keyboard.add(Text("Добавить администратора"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("Добавить менеджера"), color=KeyboardButtonColor.POSITIVE)
    return keyboard


def get_keyboard(message: Message) -> Keyboard:
    is_admin = IsPermission("Управление ботом")
    is_manager = IsPermission("Добавить помещение")

    if is_admin(message):
        return get_admin_keyboard()
    elif is_manager(message):
        return get_manager_keyboard()
    else:
        return get_main_keyboard()