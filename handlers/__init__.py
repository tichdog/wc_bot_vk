from vkbottle.bot import Bot
from handlers.admin import register_admin_handlers, register_admin_state_handlers_all
from handlers.user import register_user_handlers
from handlers.common import register_common_handlers


def register_all_handlers(bot: Bot):
    register_admin_handlers(bot)
    register_user_handlers(bot)
    register_admin_state_handlers_all(bot)
    register_common_handlers(bot)