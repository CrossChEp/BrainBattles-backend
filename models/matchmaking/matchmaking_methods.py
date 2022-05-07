from fastapi import HTTPException

from middlewares import get_redis_table
from models.matchmaking.matchmaking_auxilary_methods import generate_queue_model, search_subjects, delete_user
from store import User
import json
from configs import redis, QUEUE


def adding_to_staging(subjects: list, user: User):
    """
    adds user to queue
    :param subjects: str
    :param user: User
    :return: None
    """

    get_redis_table(table_name=QUEUE)
    queue = json.loads(redis.get(QUEUE))
    user_json = generate_queue_model(user=user, subjects=subjects)
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
    subject = search_subjects(queue=queue, user_id=user.id)
    if not subject:
        raise HTTPException(status_code=403, detail='User is not in staging')
    user_model = generate_queue_model(user=user, subject=subject)
    queue = delete_user(user_model=user_model, queue=queue)
    redis.set(QUEUE, json.dumps(queue))

