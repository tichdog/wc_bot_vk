import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from peewee import (
    SqliteDatabase, Model,
    CharField, BooleanField,
    ForeignKeyField, DateTimeField,
    IntegerField,
)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'database.db')

db = SqliteDatabase(DB_PATH, pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)

    class Meta:
        table_name = 'users'


class Role(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'roles'


class UserRole(BaseModel):
    user = ForeignKeyField(User, backref='user_roles')
    role = ForeignKeyField(Role, backref='role_users')

    class Meta:
        table_name = 'user_roles'


class Permission(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'permissions'


class RolePermission(BaseModel):
    role = ForeignKeyField(Role, backref='role_permissions')
    permission = ForeignKeyField(Permission, backref='permission_roles')

    class Meta:
        table_name = 'role_permissions'


class Room(BaseModel):
    name = CharField()
    creator = ForeignKeyField(User, backref='rooms')
    is_archived = BooleanField(default=False)

    @staticmethod
    def get_active_by_user(user_id: int) -> List['Room']:
        return list(
            Room.select().where(
                (Room.creator == user_id) &
                (Room.is_archived == False)
            )
        )

    class Meta:
        table_name = 'rooms'


class Appeal(BaseModel):
    room = ForeignKeyField(Room, backref='appeals')
    author = ForeignKeyField(User, backref='appeals')
    created_at = DateTimeField(default=datetime.now)
    message = CharField()

    class Meta:
        table_name = 'appeals'


class Notify(BaseModel):
    user = ForeignKeyField(User, backref='notifies')
    room = ForeignKeyField(Room, backref='notifies')

    class Meta:
        table_name = 'notifies'


PERMISSIONS = [
    "Добавить помещение",
    "Список помещений",
    "Добавить администратора",
    "Управление ботом",
    "Особое приветствие",
    "Добавить менеджера",
]

ROLES = [
    "Администратор",
    "Менеджер",
]

ROLE_PERMISSIONS = [
    ("Администратор", "Добавить помещение"),
    ("Администратор", "Список помещений"),
    ("Администратор", "Добавить администратора"),
    ("Администратор", "Управление ботом"),
    ("Администратор", "Особое приветствие"),
    ("Администратор", "Добавить менеджера"),

    ("Менеджер", "Добавить помещение"),
    ("Менеджер", "Список помещений"),
]

def create_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    db.connect(reuse_if_open=True)
    db.create_tables([User, Role, UserRole, Permission, RolePermission, Room, Appeal, Notify])

    load_dotenv()

    for perm_name in PERMISSIONS:
        Permission.get_or_create(name=perm_name)

    for role_name in ROLES:
        Role.get_or_create(name=role_name)

    for role_name, perm_name in ROLE_PERMISSIONS:
        RolePermission.get_or_create(
            role=Role.get(name=role_name),
            permission=Permission.get(name=perm_name),
        )

    admin_ids = list(map(int, os.getenv('ADMIN', '').split()))
    admin_role = Role.get(name="Администратор")

    for admin_id in admin_ids:
        user, _ = User.get_or_create(id=admin_id)
        UserRole.get_or_create(user=user, role=admin_role)

    db.close()