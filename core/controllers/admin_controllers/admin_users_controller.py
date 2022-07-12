from sqlalchemy.orm import Session

from core.exceptions import throw_exception_if_user_have_no_rights
from core.middlewares.database_session import generate_session
from core.models import User, get_user_by_id
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable


def ban_user_controller(ban_data: BanUserModel, user: UserTable) -> None:
    user = User(user)
    throw_exception_if_user_have_no_rights(user.ban_user, ban_data)


def edit_user_controller(user_id: int, new_user_data: UserUpdateAdminModel,
                         user: UserTable):
    user = User(user)
    throw_exception_if_user_have_no_rights(user.edit_another_user, user_id, new_user_data)


def delete_another_user_controller(user_id: int, user: UserTable) -> None:
    user = User(user)
    session: Session = next(generate_session())
    user_we_want_to_delete = get_user_by_id(user_id, session)
    throw_exception_if_user_have_no_rights(user.delete_another_user, user_we_want_to_delete)
