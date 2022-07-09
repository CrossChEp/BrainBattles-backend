from core.middlewares.database_session import generate_session
from core.models.user.user_methods import users_get


def test_users_get():
    session = next(generate_session())
    assert users_get(session)
