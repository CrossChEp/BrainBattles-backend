from sqlalchemy.orm import Session

from core.middlewares.database_session import generate_session
from core.models import get_task_by_id, User
from core.store import UserTable


def hide_task_controller(task_id: int, user: UserTable):
    user = User(user)
    user.hide_task(task_id)
