from vkbottle.bot import Bot

from handlers.admin import register_admin_handlers
from handlers.user import labeler as user_labeler
from handlers.common import labeler as common_labeler


def register_all_handlers(bot: Bot):
    register_admin_handlers(bot)
    bot.labeler.load(user_labeler)
    bot.labeler.load(common_labeler)