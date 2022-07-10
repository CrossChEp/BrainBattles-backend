from core.models import User
from core.schemas import BanUserModel
from core.store import UserTable


def ban_user_controller(ban_data: BanUserModel, user: UserTable) -> None:
    user = User(user)
    user.ban_user(ban_data)
