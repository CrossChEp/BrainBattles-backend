import json
import random

from configs import redis, QUEUE
from middlewares import create_session
from schemas.api_models import GameModel
from store import User, Task


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


def check_user_in_queue(user: User, queue: list):
    for user_place in queue:
        if user_place['user_id'] == user.id:
            return user_place


def check_user_in_game(user: User, games: list):
    for game in games:
        if game['user_id'] == user.id:
            queue = create_session(QUEUE)
            user_queue_place = check_user_in_queue(user, queue)
            if queue and user_queue_place:
                queue.pop(queue.index(user_queue_place))
                redis.set('queue', json.dumps(queue))
            return {'task': int(game['task'])}
    return False


def generate_game_model(user_id: int, opponent_id: int, task: Task):
    game_model = GameModel(
        user_id=user_id,
        opponent_id=opponent_id,
        task=task.id
    )
    return game_model


def delete_from_queue(queue: list, user_model: GameModel):
    for index, user_place in enumerate(queue):
        if user_model.dict()['user_id'] == user_place['user_id']:
            queue.pop(index)
    return queue


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
    queue = delete_from_queue(queue=queue, user_model=user_game)
    redis.set('queue', json.dumps(queue))
    return {'task': random_task.id}
