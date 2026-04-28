from vkbottle import BaseStateGroup

class AdminStates(BaseStateGroup):
    waiting_for_room_name = 0
    waiting_for_admin_id = 1
    waiting_for_manager_id = 2