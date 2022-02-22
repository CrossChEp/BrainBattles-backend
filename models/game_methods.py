import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import delete_from_staging
from store import User, Staging, Game, Task


def add_to_game(user: User, session: Session):
    staging = session.query(Staging).filter_by(user_id=user.id).first()
    staging_parameters = session.query(Staging).all()
    tasks = session.query(Task).all()
    random_task = random.randint(1, len(tasks))
    task = session.query(Task).filter_by(id=random_task).first()
    if not staging:
        raise HTTPException(status_code=403, detail='You are not in staging')
    flag = False
    opponent_id = None
    while not flag:
        if len(staging_parameters) <= 1:
            raise HTTPException(status_code=403, detail='You are only person in lobby, please wait')
        random_id = random.randint(1, len(staging_parameters))
        opponent_id = session.query(Staging).filter_by(id=random_id).first()
        if opponent_id.user_id != user.id:
            flag = True
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
    game = session.query(Game).filter_by(user_id=user.id, opponent_id=opponent.id).first()
    task.games.append(game)
    game = session.query(Game).filter_by(user_id=opponent.id, opponent_id=user.id).first()
    task.games.append(game)
    session.commit()


def leave_game(user: User, session: Session):
    session_user = session.query(Game).filter_by(user_id=user.id).first()
    session_user_opponent = session.query(Game).filter_by(opponent_id=user.id).first()
    if session_user is None or session_user_opponent is None:
        raise HTTPException(status_code=403, detail='User is not in the game')
    session.delete(session_user)
    session.delete(session_user_opponent)
    session.commit()


def make_try(answer: str, user: User, session: Session):
    game_checking = session.query(Game).filter_by(user_id=user.id).first()
    if not game_checking:
        raise HTTPException(status_code=403, detail='User is not in game')
    task = session.query(Task).filter_by(id=game_checking.task).first()
    if task.right_answer == answer:
        leave_game(user=user, session=session)
        user.scores += task.scores
        session.commit()
    raise HTTPException(status_code=400, detail='Wrong answer')
