from vkbottle.bot import Message

from models import Role, User, UserRole

# проверка роли
class IsRole:

    def __init__(self, role_name: str) -> None:
        self.role_name = role_name
        self._role = None

    @property
    def role(self):
        if self._role is None:
            self._role = Role.get_or_none(name=self.role_name)
        return self._role

    def check(self, user: User) -> bool:
        if self.role is None:
            return False
        user_role = (
            UserRole.select()
            .where(
                (UserRole.user == user) &
                (UserRole.role == self.role)
            )
            .first()
        )
        return user_role is not None

    def __call__(self, message: Message) -> bool:
        user = User.get_or_none(id=message.from_id)
        if user is None:
            return False
        return self.check(user)
