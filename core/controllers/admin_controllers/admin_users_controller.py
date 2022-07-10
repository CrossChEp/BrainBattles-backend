from core.models import User
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable


def ban_user_controller(ban_data: BanUserModel, user: UserTable) -> None:
    user = User(user)
    user.ban_user(ban_data)


def edit_user_controller(user_id: int, new_user_data: UserUpdateAdminModel,
                         user: UserTable):
    user = User(user)
    user.edit_another_user(user_id, new_user_data)
