
from ...services.user_service import UserManager

user_manager = UserManager()


user = user_manager.create_user(data)
