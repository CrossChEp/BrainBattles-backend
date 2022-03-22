from fastapi import HTTPException

from middlewares import get_redis_table
from models.matchmaking.matchmaking_middlewares import generate_queue_model, search_subject, delete_user
from store import User
import json
from configs import redis, QUEUE


def adding_to_staging(subject: str, user: User):
    """
    adds user to queue
    :param subject: str
    :param user: User
    :return: None
    """

    get_redis_table(table_name=QUEUE)
    queue = json.loads(redis.get(QUEUE))
    user_json = generate_queue_model(user=user, subject=subject)
    if user_json.dict() in queue:
        raise HTTPException(status_code=403, detail='User already in queue')
    queue.append(user_json.dict())
    redis.set('queue', json.dumps(queue))


def delete_from_staging(user: User):
    """
    deletes user from queue(redis)
    :param user: User
    :return: None
    """

    get_redis_table(table_name=QUEUE)
    queue = json.loads(redis.get(QUEUE))
    subject = search_subject(queue=queue, user_id=user.id)
    if not subject:
        raise HTTPException(status_code=403, detail='User is not in staging')
    user_model = generate_queue_model(user=user, subject=subject)
    queue = delete_user(user_model=user_model, queue=queue)
    redis.set(QUEUE, json.dumps(queue))

