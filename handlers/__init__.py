from vkbottle.bot import Bot

from handlers.role import register_admin_handlers
from handlers.user import labeler as user_labeler
from handlers.common import labeler as common_labeler
from handlers.command import labeler as command_labeler
from handlers.room.add import labeler as add_room_labeler
from handlers.room.get import labeler as get_room_labeler


def register_all_handlers(bot: Bot):
    register_admin_handlers(bot)
    bot.labeler.load(user_labeler)
    bot.labeler.load(command_labeler)
    bot.labeler.load(add_room_labeler)
    bot.labeler.load(get_room_labeler)
    bot.labeler.load(common_labeler) # Всегда последний