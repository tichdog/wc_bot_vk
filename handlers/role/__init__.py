from vkbottle.bot import Bot

from handlers.role.add_role import labeler as role_labeler


def register_admin_handlers(bot: Bot):
    bot.labeler.load(role_labeler)