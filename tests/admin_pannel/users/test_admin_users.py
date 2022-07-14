from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs import BANNED
from core.controllers import ban_user_controller
from core.middlewares.database_session import generate_session
from core.models import get_user_by_id, delete_user_from_database
from core.schemas import BanUserModel


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
