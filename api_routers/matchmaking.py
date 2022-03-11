from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from models import adding_to_staging, delete_from_staging
from store import User, get_session

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_staging(subject: str, user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """ POST endpoint that adds user to queue
    :param subject: str
    :param user: User
    :param session: Session
    :return: Json
    """

    return adding_to_staging(subject=subject, user=user)


@matchmaking_router.delete('/api/matchmaking')
def staging_cancel(user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """ DELETE endpoint that deletes user from queue

    :param user: User
    :param session: Session
    :return: Json
    """

    return delete_from_staging(user=user, session=session)