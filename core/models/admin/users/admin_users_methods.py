from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.configs import BANNED, DEFAULT
from core.configs.config import OPEN
from core.models.user.user_methods import get_user_by_id
from core.schemas import BanUserModel
from core.store import UserTable


def update_user_data_to_banned(ban_data: BanUserModel, session: Session) -> None:
    user = get_user_by_id(ban_data.id, session)
    user.state = BANNED
    user.ban_term = ban_data.term
    session.commit()


def ban_user_temporary(ban_data: BanUserModel, session: Session) -> None:
    if not ban_data.term:
        raise HTTPException(status_code=403, detail="You should specify the term")

    update_user_data_to_banned(ban_data, session)


def ban_user_permanently(ban_data: BanUserModel, session: Session) -> None:
    if not ban_data.term:
        ban_data.term = datetime.now() + relativedelta(years=100)

    update_user_data_to_banned(ban_data, session)


def unban_user(user: UserTable, session: Session) -> None:
    user.state = DEFAULT
    user.ban_term = None
    session.commit()
