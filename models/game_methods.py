import json
import random

import redis
from fastapi import HTTPException
from sqlalchemy.orm import Session

from configs import ranks, QUEUE, GAME, redis
from middlewares import create_session
from models.game_adding_subject_methods import get_random_user, adding_user_to_game, check_user_in_game
from models.game_adding_subject_methods import filtered_users, get_random_task, \
    database_task_adding
from models.matchmaking_middlewares import generate_queue_model, search_subject
from schemas.api_models import GameModel
from store import User, Staging, Game, Task
from models.game_adding_rank_methods import filter_by_rank


def user_adding(user: User, queue: list,
                subject: str, session: Session):
    """
    adds user to database
    :param user_staging:
    :param user: User
    :param session: Session
    :return: int
    """
    create_session(table_name=GAME)
    game = json.loads(redis.get(GAME))
    checking = check_user_in_game(user=user, games=game)
    while True:
        if checking:
            return checking
        opponents = filtered_users(subject=subject, queue=queue)
        opponents = filter_by_rank(users=opponents, active_user=user)
        if not opponents:
            continue
        opponent = get_random_user(users=opponents)
        if not opponent:
            continue
        tasks = session.query(Task).filter_by(subject=subject).all()
        if not tasks:
            raise HTTPException(status_code=404, detail='No task with such subject')
        random_task = get_random_task(tasks)
        if not random_task:
            raise HTTPException(status_code=404, detail='No task with such subject')
        task = adding_user_to_game(user=user, opponent=opponent, random_task=random_task)
        return task


def add_to_game(user: User, session: Session):
    """
    adds user to game
    :param user: User
    :param session: Session
    :return: dict
    """
    create_session(table_name=QUEUE)
    queue = json.loads(redis.get(QUEUE))
    subject = search_subject(queue=queue, user_id=user.id)
    if not subject:
        raise HTTPException(status_code=403, detail='User not in queue')
    opponents = filtered_users(subject=subject, queue=queue)
    opponents = filter_by_rank(users=opponents, active_user=user)
    task = user_adding(user=user, queue=opponents, subject=subject, session=session)
    return task


def leave_game(user: User, session: Session):
    """
    deletes user from game
    :param user: User
    :param session: Session
    :return: None
    """
    session_user = session.query(Game).filter_by(user_id=user.id).first()
    session_user_opponent = session.query(Game).filter_by(opponent_id=user.id).first()
    if session_user is None or session_user_opponent is None:
        raise HTTPException(status_code=403, detail='User is not in the game')
    session.delete(session_user)
    session.delete(session_user_opponent)
    session.commit()


def make_try(answer: str, user: User, session: Session):
    """
    makes try
    :param answer: str
    :param user: User
    :param session: Session
    :return: None
    """
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
