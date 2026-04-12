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

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'database.db')

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):

    id = IntegerField(primary_key=True)

    class Meta:
        table_name = 'users'


class Role(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'roles'


class UserRole(BaseModel):
    user = ForeignKeyField(User, backref='roles')
    role = ForeignKeyField(Role, backref='users')

    class Meta:
        table_name = 'user_roles'


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


def create_tables():
    # создать таблицы с админами
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with db:
        db.create_tables([User, Role, UserRole, Room, Appeal, Notify])

    admin_role, _ = Role.get_or_create(name='Администратор')

    load_dotenv()
    admin_ids = list(map(int, os.getenv('ADMIN', '').split()))
    for admin_id in admin_ids:
        user, _ = User.get_or_create(id=admin_id)
        UserRole.get_or_create(user=user, role=admin_role)
