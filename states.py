from vkbottle import BaseStateGroup

class AdminStates(BaseStateGroup):
    waiting_for_room_name = 0
    waiting_for_admin_id = 1