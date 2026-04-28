from vkbottle.bot import Message
from models import User


def get_or_create_user(message: Message) -> User:
    user = User.get_or_none(id=message.from_id)
    if not user:
        user = User.create(id=message.from_id)
    return user