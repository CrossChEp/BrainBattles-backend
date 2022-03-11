from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import UserQueueModel
from store import User, Staging
import json
from configs import redis


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
    staging = session.query(Staging).filter_by(user_id=user.id).first()
    if not staging:
        raise HTTPException(status_code=403, detail='User is not in staging')
    session.delete(staging)
    session.commit()