from vkbottle import Keyboard, Text, KeyboardButtonColor


def get_main_keyboard() -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("Привет"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("ID"),     color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Помощь"), color=KeyboardButtonColor.SECONDARY)
    return keyboard


def get_admin_menu() -> Keyboard:
    keyboard = get_main_keyboard()
    keyboard.row()
    keyboard.add(Text("Добавить помещение"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Список помещений"),   color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Добавить администратора"), color=KeyboardButtonColor.POSITIVE)
    return keyboard