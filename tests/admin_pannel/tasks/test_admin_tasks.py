from sqlalchemy.orm import Session

from core.configs.config import HIDDEN, OPEN
from core.controllers import hide_task_controller, add_task_to_public_controller
from core.middlewares.database_session import generate_session
from core.models import get_task_by_id, get_concrete_task_with_every_state, delete_user_from_database, get_user_by_id
from core.models.tasks.tasks_methods import delete_task
from core.store import UserTable, TaskTable


def test_tasks_hiding(give_test_user_account_with_open_task):
    session: Session = next(generate_session())
    user = get_user_by_id(give_test_user_account_with_open_task.id, session)
    task_id = user.tasks[0].id
    hide_task_controller(task_id, user)
    session.commit()
    task = session.query(TaskTable).filter_by(id=task_id).first()
    print(task.state)
    assert user.tasks[0]
    assert task.state == HIDDEN
    delete_task(task.id, session)
    delete_user_from_database(user, session)
    session.commit()


def test_adding_task_to_public(give_test_user_account_with_task):
    session: Session = next(generate_session())
    user = get_user_by_id(give_test_user_account_with_task.id, session)
    task_id = user.tasks[0].id
    add_task_to_public_controller(task_id, user)
    session.commit()
    assert user.tasks[0]
    assert user.tasks[0].state == OPEN
    delete_task(user.tasks[0].id, session)
    delete_user_from_database(user, session)

