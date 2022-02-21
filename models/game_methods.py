import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from store import User, Staging


def add_to_game(user: User, session: Session):
    staging = session.query(Staging).filter_by(user_id=user.id).first()
    if not staging:
        raise HTTPException(status_code=403)
    flag = False
    random_id = None
    while not flag:
        random_id = random.randint(0, len(staging))
        if random_id != user.id:
            flag = True
    opponent_staging = session.query(Staging).filter_by(user_id=random_id).first()
