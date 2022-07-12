from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.configs import BANNED, DEFAULT
from core.exceptions import throw_exception_if_user_have_no_rights, throw_exception_if_user_have_lesser_state
from core.models.user.user_methods import get_user_by_id, update_user_data
from core.schemas import BanUserModel, UserUpdateAdminModel
from core.store import UserTable


def update_user_data_to_banned(user: UserTable, ban_data: BanUserModel,
                               session: Session) -> None:
    user.state = BANNED
    user.ban_term = ban_data.term
    session.commit()


def ban_user_temporary(ban_author: UserTable, ban_data: BanUserModel,
                       session: Session) -> None:
    if not ban_data.term:
        raise HTTPException(status_code=403, detail="You should specify the term")

    ban_author = get_user_by_id(ban_author.id, session)
    user = get_user_by_id(ban_data.id, session)
    throw_exception_if_user_have_lesser_state(ban_author, user)
    update_user_data_to_banned(user, ban_data, session)


def ban_user_permanently(ban_author: UserTable, ban_data: BanUserModel,
                          session: Session) -> None:
    if not ban_data.term:
        ban_data.term = datetime.now() + relativedelta(years=100)

    ban_author = get_user_by_id(ban_author.id, session)
    user = get_user_by_id(ban_data.id, session)
    throw_exception_if_user_have_lesser_state(ban_author, user)
    update_user_data_to_banned(user, ban_data, session)


def unban_user(user: UserTable, session: Session) -> None:
    user.state = DEFAULT
    user.ban_term = None
    session.commit()


def edit_user(user: UserTable, update_data: UserUpdateAdminModel, session: Session):
    update_user_data(user, update_data, session)


def promote_user(promotion_method, user_id: int,
                 session: Session):
    user_we_want_to_promote = get_user_by_id(user_id, session)
    throw_exception_if_user_have_no_rights(promotion_method, user_we_want_to_promote)


def promote_user_to_anther_state(user: UserTable, promoter: UserTable,
                                 state: str, session: Session):
    promoter = get_user_by_id(promoter.id, session)
    throw_exception_if_user_have_lesser_state(promoter, user)
    user.state = state
    session.commit()
