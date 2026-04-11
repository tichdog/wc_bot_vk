from vkbottle.bot import Bot
from handlers.user import register_user_handlers
from handlers.common import register_common_handlers


def register_all_handlers(bot: Bot):
    # Порядок важен: специфичные хэндлеры — до fallback
    register_user_handlers(bot)
    register_common_handlers(bot)