from vkbottle import BaseStateGroup
from vkbottle.dispatch.dispenser.builtin import BuiltinStateDispenser

class AdminStates(BaseStateGroup):
    waiting_for_room_name = 0
    waiting_for_admin_id = 1
    waiting_for_manager_id = 2

state_dispenser = BuiltinStateDispenser()
