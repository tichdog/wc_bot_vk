from vkbottle.bot import Bot

from handlers.admin.command import register_admin_command_handlers
from handlers.admin.room import register_admin_room_handlers, register_admin_state_handlers


def register_admin_handlers(bot: Bot):
    register_admin_command_handlers(bot)
    register_admin_room_handlers(bot)


def register_admin_state_handlers_all(bot: Bot):
    register_admin_state_handlers(bot)