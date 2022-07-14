from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from prompt_toolkit.key_binding.bindings.named_commands import edit_and_execute
from sqlalchemy.orm import Session

from core.configs import BANNED
from core.controllers import ban_user_controller, edit_user_controller
from core.middlewares.database_session import generate_session
from core.models import get_user_by_id, delete_user_from_database
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable
from tests.admin_pannel.users.conftest import new_user_data


def check_new_user_data(user: UserTable):
    assert user.nickname == new_user_data['nickname']
    assert user.email == new_user_data['email']
    assert user.name == new_user_data['name']
    assert user.surname == new_user_data['surname']
    assert user.rank == new_user_data['rank']
    assert user.wins == new_user_data['wins']
    assert user.scores == new_user_data['scores']
    assert user.games == new_user_data['games']


def test_temporary_ban(give_moderator_user):
    first_user = give_moderator_user[0]
    second_user = give_moderator_user[1]
    session: Session = next(generate_session())
    first_user = get_user_by_id(first_user.id, session)
    second_user = get_user_by_id(second_user.id, session)
    with pytest.raises(HTTPException):
        ban_user = ban_user_controller(BanUserModel(id=second_user.id), first_user) == HTTPException
    ban_date = datetime.now() + relativedelta(days=1)
    ban_user_controller(BanUserModel(id=second_user.id, term=ban_date), first_user)
    session.commit()
    assert second_user.state == BANNED
    assert second_user.ban_term == ban_date
    delete_user_from_database(first_user, session)
    delete_user_from_database(second_user, session)


def test_permanent_ban(give_admin_user):
    first_user = give_admin_user[0]
    second_user = give_admin_user[1]
    session: Session = next(generate_session())
    first_user = get_user_by_id(first_user.id, session)
    second_user = get_user_by_id(second_user.id, session)
    ban_user_controller(BanUserModel(id=second_user.id), first_user)
    session.commit()
    assert second_user.state == BANNED
    assert second_user.ban_term
    delete_user_from_database(first_user, session)
    delete_user_from_database(second_user, session)


def test_user_editing(give_admin_user):
    first_user = give_admin_user[0]
    second_user = give_admin_user[1]
    session: Session = next(generate_session())
    first_user = get_user_by_id(first_user.id, session)
    second_user = get_user_by_id(second_user.id, session)
    edit_user_controller(second_user.id, UserUpdateAdminModel(**new_user_data), first_user)
    session.commit()
    check_new_user_data(second_user)
    delete_user_from_database(first_user, session)
    delete_user_from_database(second_user, session)
