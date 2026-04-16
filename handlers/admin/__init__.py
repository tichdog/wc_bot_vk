from vkbottle.bot import Bot

from handlers.admin.command import labeler as command_labeler
from handlers.admin.room import labeler as room_labeler
from handlers.admin.admin_mgmt import labeler as admin_mgmt_labeler


def register_admin_handlers(bot: Bot):
    bot.labeler.load(command_labeler)
    bot.labeler.load(room_labeler)
    bot.labeler.load(admin_mgmt_labeler)