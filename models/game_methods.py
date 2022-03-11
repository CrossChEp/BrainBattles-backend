import json
import random

import redis
from fastapi import HTTPException
from sqlalchemy.orm import Session

from configs import ranks, QUEUE, GAME, redis
from middlewares import create_session
from models.game_adding_subject_methods import filtered_users, search_opponent, get_random_task, database_users_adding, \
    database_task_adding
from models.matchmaking_middlewares import generate_queue_model, search_subject
from schemas.api_models import GameModel
from store import User, Staging, Game, Task
from models.game_adding_rank_methods import filter_by_rank


def user_adding(user: User, queue: list, game: list):
    """
    adds user to database
    :param user_staging:
    :param user: User
    :param session: Session
    :return: int
    """
    random_user = None
    flag = False
    while not flag:
        random_index = random.randint(0, len(queue) - 1)
        try:
            random_user = queue[random_index]
            if random_user['user_id'] != user.id:
                flag = True
        except IndexError:
            pass
    user_game_model = GameModel(
        user_id=user.id,
        opponent_id=random_user['user_id']
    )
    opponent_game_model = GameModel(
        user_id=random_user['user_id'],
        opponent_id=user.id
    )
    queue.append(user_game_model)
    queue.append(opponent_game_model)
    # while True:
    #     users_filtered_by_subject = filtered_users(subject=user_staging.subject, session=session)
    #     users_filtered = filter_by_rank(users=users_filtered_by_subject, user=user)
    #     if not users_filtered:
    #         continue
    #     random_user = search_opponent(users=users_filtered, user=user)
    #     opponent = session.query(User).filter_by(id=random_user.user_id).first()
    #     tasks = session.query(Task).filter_by(subject=user_staging.subject).all()
    #     random_task = get_random_task(tasks=tasks)
    #     if not random_task:
    #         raise HTTPException(status_code=404, detail='No task with such subject')
    #     database_users_adding(user=user, opponent=opponent, session=session)
    #     database_task_adding(task=random_task, user_id=user.id,
    #                          opponent_id=opponent.id, session=session)
    #     return random_task.id


def add_to_game(user: User):
    """
    adds user to game
    :param user: User
    :param session: Session
    :return: dict
    """

    # game = session.query(Game).filter_by(user_id=user.id).first()
    # if game:
    #     return {'task': game.task}
    # user_staging = session.query(Staging).filter_by(user_id=user.id).first()
    # if not user_staging:
    #     raise HTTPException(status_code=403, detail='User not in queue')
    # adding = user_adding(user_staging=user_staging, user=user, session=session)
    # return {'task': adding}
    create_session(table_name=GAME)
    create_session(table_name=QUEUE)
    queue = redis.get(QUEUE)
    subject = search_subject(queue=queue, user_id=user.id)
    user_model = generate_queue_model(user=user, subject=subject)
    if user_model not in queue:
        raise HTTPException(status_code=403, detail='User not in queue')
    games = json.loads(redis.get(GAME))


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
