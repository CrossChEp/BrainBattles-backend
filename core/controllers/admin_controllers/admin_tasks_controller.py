from core.exceptions import throw_exception_if_user_have_no_rights
from core.middlewares.database_session import generate_session
from core.models import User, get_user_by_id
from core.store import UserTable


def hide_task_controller(task_id: int, user: UserTable):
    user = User(user)
    throw_exception_if_user_have_no_rights(user.hide_task, task_id)


def add_task_to_public_controller(task_id: int, user: UserTable):
    user = User(user)
    throw_exception_if_user_have_no_rights(user.add_task_to_public, task_id)
