import random

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from configs import ranks
from models import delete_from_staging
from store import User, Staging, Game, Task


def add_ranks_list(ranks: dict) -> list:
    ranks_list = []
    for key, value in ranks.items():
        ranks_list.append(value)
    return ranks_list


def add_to_game(user: User, session: Session):
    staging = session.query(Staging).filter_by(user_id=user.id).first()
    if not staging:
        raise HTTPException(status_code=403, detail='You are not in staging')
    all_ranks = add_ranks_list(ranks=ranks)
    concrete_ranks = []
    for index, rank in enumerate(all_ranks):
        if rank == user.rank:
            try:
                concrete_ranks.append(all_ranks[index - 1])
                concrete_ranks.append(rank)
                concrete_ranks.append(all_ranks[index+1])
            except IndexError:
                continue
    staging_without_rank = session.query(Staging).filter_by(
        subject=staging.subject
    ).all()
    staging_parameters = [
        stage for stage in staging_without_rank
        if stage.rank == concrete_ranks[0] or
        stage.rank == concrete_ranks[1] or
        stage.rank == concrete_ranks[2]
    ]

    if len(staging_parameters) <= 1:
        raise HTTPException(status_code=403, detail='You are only person in lobby, please wait')
    tasks = session.query(Task).filter_by(subject=staging.subject).all()
    if not tasks:
        raise HTTPException(status_code=404, detail='No tasks found')
    random_task = random.randint(1, len(tasks))
    task = session.query(Task).filter_by(id=random_task).first()
    flag = False
    opponent_id = None
    while not flag:
        ids = [user_id[0] for user_id in session.query(Staging.id)]
        random_id = random.randint(ids[0], ids[-1])
        opponent_id = session.query(Staging).filter_by(id=random_id).first()
        if opponent_id and opponent_id.user_id != user.id:
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
    return {'task': task.id}


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
        scores = list(ranks.keys())
        for index, score in enumerate(scores):
            try:
                if user.scores < scores[index + 1]:
                    new_rank = ranks[score]
                    user.rank = new_rank
                    break
            except IndexError:
                pass
        session.commit()
        return
    raise HTTPException(status_code=400, detail='Wrong answer')
