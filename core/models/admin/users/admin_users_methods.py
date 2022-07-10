from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs import BANNED, DEFAULT
from core.configs.config import OPEN
from core.models.user.user_methods import get_user_by_id
from core.schemas import BanUserModel
from core.store import UserTable


def ban_user_temporary(ban_data: BanUserModel, session: Session) -> None:
    if not ban_data.term:
        raise HTTPException(status_code=403, detail="You should specify the term")

    user = get_user_by_id(ban_data.id, session)
    user.state = BANNED
    user.ban_term = ban_data.term
    session.commit()


def unban_user(user: UserTable, session: Session) -> None:
    user.state = DEFAULT
    user.ban_term = None
    session.commit()
