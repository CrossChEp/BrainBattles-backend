import json

from sqlalchemy.orm import Session

from configs import redis
from models import delete_from_staging
from schemas.api_models import GameModel
from store import Staging, User, Game, Task
import random


def filtered_users(subject: str, queue: list):
    """
    filters users int queue regarding user's subject
    :param subject: int
    :param session: Session
    :return: list
    """
    res = []
    for user in queue:
        if user['subject'] == subject:
            res.append(user)
    return res


def get_random_user(users: list):
    """
    gets random user from queue
    :param users: list
    :return: bool, User
    """
    random_id = random.randint(0, len(users))
    try:
        random_user = users[random_id]
        return random_user
    except IndexError:
        return False


def check_user_in_game(user: User, games: list):
    for game in games:
        if game['user_id'] == user.id:
            return {'task': int(game['task'])}
    return False


def generate_game_model(user_id: int, opponent_id: int, task: Task):
    game_model = GameModel(
        user_id=user_id,
        opponent_id=opponent_id,
        task=task.id
    )
    return game_model


def adding_user_to_game(user: User, opponent: dict, random_task: Task):
    user_game = generate_game_model(user_id=user.id,
                                    opponent_id=opponent['user_id'], task=random_task)
    opponent_game = generate_game_model(user_id=opponent['user_id'],
                                        opponent_id=user.id, task=random_task)
    games = json.loads(redis.get('game'))
    games.append(user_game.dict())
    games.append(opponent_game.dict())
    redis.set('game', json.dumps(games))
    queue = json.loads(redis.get('queue'))
    for index, user_place in enumerate(queue):
        if user_game.dict()['user_id'] == user_place['user_id']:
            queue.pop(index)
    redis.set('queue', json.dumps(queue))
    return {'task': random_task.id}


def get_random_task(tasks: list):
    """
    gets random task regarding users' subject
    :param tasks: list
    :return: Task, bool
    """
    random_task_index = random.randint(0, len(tasks) - 1)
    try:
        random_task = tasks[random_task_index]
        return random_task
    except IndexError:
        return False


def database_task_adding(task: Task, user_id: int,
                         opponent_id: int, session: Session):
    """
    adds task to game database
    :param task: Task
    :param user_id: int
    :param opponent_id: int
    :param session: Session
    :return: None
    """
    user_game = session.query(Game).filter_by(user_id=user_id, opponent_id=opponent_id).first()
    opponent_game = session.query(Game).filter_by(user_id=opponent_id, opponent_id=user_id).first()
    task.games.append(user_game)
    task.games.append(opponent_game)
    session.commit()