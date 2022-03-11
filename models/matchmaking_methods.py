from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import UserQueueModel
from store import User
import json
from configs import redis


def generate_queue_model(user: User, subject: str) -> UserQueueModel:
    user_json = UserQueueModel(
        user_id=user.id,
        subject=subject,
        rank=user.rank
    )
    return user_json


def search_subject(queue: list, user_id: int):
    subject = str()
    for user in queue:
        if user['user_id'] == user_id:
            subject = user['subject']
    return subject


def adding_to_staging(subject: str, user: User):
    """
    adds user to queue
    :param subject: str
    :param user: User
    :param session: Session
    :return:
    """

    try:
        redis.get('queue')
    except TypeError:
        redis.set('queue', json.dumps([]))
    queue = json.loads(redis.get('queue'))

    user_json = UserQueueModel(
        user_id=user.id,
        subject=subject,
        rank=user.rank
    )
    if user_json.dict() in queue:
        raise HTTPException(status_code=403, detail='User already in queue')
    queue.append(user_json.dict())
    redis.set('queue', json.dumps(queue))


def delete_from_staging(user: User, session: Session):
    """
    deletes user from queue
    :param user: User
    :param session: Session
    :return:
    """
    # staging = session.query(Staging).filter_by(user_id=user.id).first()
    # if not staging:
    #     raise HTTPException(status_code=403, detail='User is not in staging')
    # session.delete(staging)
    # session.commit()

    try:
        redis.get('queue')
    except TypeError:
        redis.set('queue', json.dumps([]))
    queue = json.loads(redis.get('queue'))
    subject = search_subject(queue=queue, user_id=user.id)
    if not subject:
        raise HTTPException(status_code=403, detail='User is not in staging')
    user_model = generate_queue_model(user=user, subject=subject)
    for user in range(len(queue)):
        if user_model == queue[user]:
            queue.pop(user)
    redis.set('queue', json.dumps(queue))

