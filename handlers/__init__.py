from vkbottle.bot import Bot
from handlers.admin import register_admin_handlers, register_admin_state_handlers_all
from handlers import user
from handlers.common import register_common_handlers


def register_all_handlers(bot: Bot):
    register_admin_handlers(bot)
    bot.set_blueprints(
        user.bp,
    )
    register_admin_state_handlers_all(bot)
    register_common_handlers(bot)