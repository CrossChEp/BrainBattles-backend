from core.models import User
from core.schemas import UserUpdateModel, UserAbstractModel
from core.store import UserTable


def get_all_users_controller(user: UserTable):
    user = User(user)
    return user.get_users()


def delete_user_controller(user: UserTable):
    user = User(user)
    user.delete()


def update_user_data_controller(user: UserTable, new_user_data: UserUpdateModel):
    user = User(user)
    user.update(new_user_data)


def get_user_by_id_controller(user: UserTable, user_id: int):
    user = User(user)
    return user.get_user(UserAbstractModel(id=user_id))
