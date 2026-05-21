from vkbottle.bot import Message
from vkbottle.tools.mini_types.bot import MessageMin
from vkbottle import ABCRule

from models import Permission, RolePermission, User, UserRole


class IsPermission(ABCRule[MessageMin]):
    def __init__(self, permission_name: str) -> None:
        self.permission_name = permission_name
        self._permission: Permission | None = None

    @property
    def permission(self) -> Permission | None:
        if self._permission is None:
            self._permission = Permission.get_or_none(name=self.permission_name)
        return self._permission

    def _check_user(self, user: User) -> bool:
        if self.permission is None:
            return False
        return (
            RolePermission
            .select()
            .join(UserRole, on=(UserRole.role == RolePermission.role))
            .where(
                (UserRole.user == user) &
                (RolePermission.permission == self.permission)
            )
            .exists()
        )

    async def check(self, message: MessageMin) -> bool:
        user = User.get_or_none(id=message.from_id)
        if user is None:
            return False
        return self._check_user(user)

