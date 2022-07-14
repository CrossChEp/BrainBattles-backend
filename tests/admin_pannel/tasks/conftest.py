import pytest
from sqlalchemy.orm import Session

from core.api_routers.tasks import add_task
from core.configs import ADMIN
from core.configs.config import OPEN
from core.middlewares.database_session import generate_session
from core.models import add_user_to_database, get_user, task_add
from core.schemas import UserRegisterModel, UserAbstractModel, TaskAddModel
from core.store import UserTable, TaskTable

test_user_data = {
    'nickname': 'testUser',
    'email': 'test_user@gmail.com',
    'name': 'testUser',
    'surname': 'testUser',
    'password': 'testUser',
}


test_task_data = {
    'name': 'testTask',
    'subject': 'math',
    'content': 'testTask',
    'right_answer': 'testTask',
    'scores': 0,
    'rank': 'rank 10',
}


def promote_test_user_to_admin(user: UserTable, session: Session):
    user.state = ADMIN
    session.commit()


def add_task_to_public(task: TaskTable, session: Session):
    task.state = OPEN
    session.commit()


@pytest.fixture
def give_test_user_account_with_open_task():
    session: Session = next(generate_session())
    add_user_to_database(UserRegisterModel(**test_user_data), session)
    test_user: UserTable = get_user(UserAbstractModel(nickname=test_user_data['nickname']), session)
    promote_test_user_to_admin(test_user, session)
    task_add(TaskAddModel(**test_task_data), test_user, session)
    add_task_to_public(test_user.tasks[0], session)
    yield test_user


@pytest.fixture
def give_test_user_account_with_task():
    session: Session = next(generate_session())
    add_user_to_database(UserRegisterModel(**test_user_data), session)
    test_user: UserTable = get_user(UserAbstractModel(nickname=test_user_data['nickname']), session)
    promote_test_user_to_admin(test_user, session)
    task_add(TaskAddModel(**test_task_data), test_user, session)
    yield test_user
