from core.models import User
from core.store import UserTable


def get_all_users_controller(user: UserTable):
    user = User(user)
    return user.get_users()


def delete_user_controller(user: UserTable):
    user = User(user)
    user.delete()
