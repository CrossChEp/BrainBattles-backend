import json
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session, create_session

from core.configs import redis, QUEUE, GAME, ranks
from core.middlewares import get_redis_table
from core.models import get_user_by_id
from core.schemas import GameModel
from core.store import UserTable, TaskTable


def find_game(user: UserTable, games: list):
    """ finds user's game
    :param user: User
    :param games: List[GameModel]
    :return game, None: GameModel, None
    """

    for game in games:
        if game['user_id'] == user.id:
            return game
    return None


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


def check_user_in_queue(user: UserTable, queue: list):
    """ Checks if user in queue
        and if yes, returns user's place

    :param user: User
    :param queue: List[QueueModel]
    :return user_place, False: QueueMode, bool

    """
    for user_place in queue:
        if user_place['user_id'] == user.id:
            return user_place
    return False


def check_user_in_game(user: UserTable, games: list):
    """ Checks if user in games
        and if yes, returns game task
    :param user: User
    :param games: List[GameModel]
    :return dict, False: dict, bool

    """

    for game in games:
        if game['user_id'] == user.id:
            queue = get_redis_table(QUEUE)
            user_queue_place = check_user_in_queue(user, queue)
            if queue and user_queue_place:
                queue.pop(queue.index(user_queue_place))
                redis.set('queue', json.dumps(queue))
            return GameModel(
                user_id=game['user_id'],
                opponent_id=game['opponent_id'],
                task=int(game['task'])
            )
    return False


def generate_game_model(user_id: int, opponent_id: int, task: TaskTable):
    """ generates game model using user id,
        opponent id and task

    :param user_id: int
    :param opponent_id: int
    :param task: Task
    :return game_model: GameModel

    """
    game_model = GameModel(
        user_id=user_id,
        opponent_id=opponent_id,
        task=int(task.id)
    )
    return game_model


def delete_from_queue(queue: list, user_model: GameModel):
    """ deletes user from queue
    :param queue: List[QueueModel]
    :param user_model: GameModel
    :return queue: List[QueueModel]

    """
    for index, user_place in enumerate(queue):
        if user_model.dict()['user_id'] == user_place['user_id']:
            queue.pop(index)
    return queue


def adding_user_to_game(user: UserTable, opponent: dict, random_task: TaskTable):
    """ adds user to game
    :param user: User
    :param opponent: dict
    :param random_task: Task
    :return: dict

    """
    user_game = generate_game_model(user_id=user.id,
                                    opponent_id=opponent['user_id'], task=random_task)
    opponent_game = generate_game_model(user_id=opponent['user_id'],
                                        opponent_id=user.id, task=random_task)
    games = get_redis_table(GAME)
    games.append(user_game.dict())
    games.append(opponent_game.dict())
    redis.set('game', json.dumps(games))
    queue = get_redis_table(QUEUE)
    queue = delete_from_queue(queue=queue, user_model=user_game)
    redis.set('queue', json.dumps(queue))
    return user_game


def winner_exists(game: dict):
    """ checks if winner already exists in game
    :param game: dict
    :return: bool
    """
    if game['winner']:
        return True
    return False


def set_winner(game: dict, user: UserTable, session: Session):
    """sets winner to the user game and opponent game
    :param game: dict
        user's game
    :param user: User
        current user
    :param session: Session
    """
    games = get_redis_table(GAME)
    opponent = get_user_by_id(uid=game['opponent_id'], session=session)
    opponent_game = find_game(user=opponent, games=games)
    if opponent_game:
        opponent_game['winner'] = user.id
    game['winner'] = user.id
    for special_game in games:
        if special_game == game:
            special_game = game
        elif special_game == opponent_game:
            special_game = opponent_game

    redis.set(GAME, json.dumps(games))


def winner_check(user: UserTable) -> bool:
    """ checks if user winner or
        has the opponent already won
    :param user: User
        current user
    :return: bool
    """

    games = get_redis_table(GAME)
    game = find_game(user=user, games=games)
    if not game:
        raise HTTPException(status_code=403, detail='User not in game')
    if winner_exists(game):
        if game['winner'] != user.id:
            return True
    return False


def set_user_rank(scores: list, user: UserTable):
    """Sets user rank that equal to his scores

    :param scores: list
        (all ranks' scores)
    :param user: User
    :return:
    """
    for index, score in enumerate(scores):
        try:
            if user.scores < scores[index + 1]:
                new_rank = ranks[score]
                user.rank = new_rank
                break
        except IndexError:
            pass
