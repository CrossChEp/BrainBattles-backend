from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs import BANNED
from core.models.user.user_methods import get_user_by_id
from core.schemas import BanUserModel


def ban_user_temporary(ban_data: BanUserModel, session: Session) -> None:
    if not ban_data.term:
        raise HTTPException(status_code=403, detail="You should specify the term")

    user = get_user_by_id(ban_data.id, session)
    user.state = BANNED
    user.ban_term = datetime.now()
    session.commit()
