from fastapi import HTTPException
from sqlalchemy.orm import Session

from store import User, Staging

from configs import redis


def adding_to_staging(subject: str, user: User, session: Session):
    """
    adds user to queue
    :param subject: str
    :param user: User
    :param session: Session
    :return:
    """
    # is_staging_exists = session.query(Staging).filter_by(user_id=user.id).all()
    # if is_staging_exists:
    #     raise HTTPException(status_code=403, detail='User already in staging')
    # staging = Staging(
    #     user_id=user.id,
    #     rank=user.rank,
    #     subject=subject
    # )
    # session.add(staging)
    # user.staging.append(staging)
    # session.commit()
    is_staging_exists = redis.jsonget('queue')




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