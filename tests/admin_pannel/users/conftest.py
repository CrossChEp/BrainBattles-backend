import pytest
from sqlalchemy.orm import Session

from core.configs import MODERATOR, ADMIN, DEFAULT
from core.middlewares.database_session import generate_session
from core.models import add_user_to_database, get_user
from core.schemas import UserRegisterModel, UserAbstractModel
from tests.admin_pannel.tasks.conftest import promote_test_user_to_another_state

test_user_data = {
    'nickname': 'testUser',
    'email': 'test_user@gmail.com',
    'name': 'testUser',
    'surname': 'testUser',
    'password': 'testUser',
}

test_second_user_data = {
    'nickname': 'testUser2',
    'email': 'test_user2@gmail.com',
    'name': 'testUser2',
    'surname': 'testUser2',
    'password': 'testUser2',
}

new_user_data = {
    'nickname': 'testNewUser',
    'email': 'test_new_user@gmail.com',
    'name': 'testNewUser',
    'surname': 'testNewUser',
    'password': 'testNewUser',
    'rank': '5',
    'wins': 10,
    'scores': 13,
    'games': 30
}


@pytest.fixture
def give_moderator_user():
    session: Session = next(generate_session())
    add_user_to_database(UserRegisterModel(**test_user_data), session)
    add_user_to_database(UserRegisterModel(**test_second_user_data), session)
    first_user = get_user(UserAbstractModel(nickname=test_user_data['nickname']), session)
    second_user = get_user(UserAbstractModel(nickname=test_second_user_data['nickname']), session)
    promote_test_user_to_another_state(first_user, state=MODERATOR, session=session)
    promote_test_user_to_another_state(second_user, state=DEFAULT, session=session)
    yield [first_user, second_user]


@pytest.fixture
def give_admin_user():
    session: Session = next(generate_session())
    add_user_to_database(UserRegisterModel(**test_user_data), session)
    add_user_to_database(UserRegisterModel(**test_second_user_data), session)
    first_user = get_user(UserAbstractModel(nickname=test_user_data['nickname']), session)
    second_user = get_user(UserAbstractModel(nickname=test_second_user_data['nickname']), session)
    promote_test_user_to_another_state(first_user, state=ADMIN, session=session)
    promote_test_user_to_another_state(second_user, state=DEFAULT, session=session)
    yield [first_user, second_user]
