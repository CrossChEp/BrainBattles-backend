import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import delete_from_staging
from store import User, Staging, Game


def add_to_game(user: User, session: Session):
    staging = session.query(Staging).filter_by(user_id=user.id).first()
    staging_parameters = session.query(Staging).all()
    if not staging:
        raise HTTPException(status_code=403)
    flag = False
    random_id = None
    while not flag:
        if len(staging_parameters) <= 1:
            raise HTTPException(status_code=403)
        random_id = random.randint(0, len(staging_parameters))
        if random_id != user.id:
            flag = True
    opponent_id = session.query(Staging).filter_by(id=random_id).first()
    opponent = session.query(User).filter_by(id=opponent_id.user_id).first()
    opponent_game = Game(
        opponent_id=opponent.id
    )
    user_game = Game(
        opponent_id=user.id
    )
    session.add(opponent_game)
    user.game.append(opponent_game)
    session.add(user_game)
    opponent.game.append(user_game)
    session.commit()
    delete_from_staging(user=user, session=session)
    delete_from_staging(user=opponent, session=session)
