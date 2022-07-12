from sqlalchemy.orm import Session

from core.configs.config import HIDDEN
from core.controllers import hide_task_controller
from core.middlewares.database_session import generate_session
from core.models import get_task_by_id, get_concrete_task_with_every_state, delete_user_from_database, get_user_by_id
from core.models.tasks.tasks_methods import delete_task
from core.store import UserTable, TaskTable


def test_tasks_hiding(give_test_user_account: UserTable):
    session: Session = next(generate_session())
    user = get_user_by_id(give_test_user_account.id, session)
    task_id = user.tasks[0].id
    hide_task_controller(task_id, user)
    print(user.tasks[0].state)
    assert user.tasks[0]
    assert user.tasks[0].state == HIDDEN
    delete_task(user.tasks[0].id, session)
    delete_user_from_database(user, session)

