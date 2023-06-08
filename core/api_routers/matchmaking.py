from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.api_routers.auth import get_current_user
from core.models import adding_to_staging, delete_from_staging
from core.store import UserTable

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_staging(subjects: list, user: UserTable = Depends(get_current_user)):
    """ POST endpoint that adds user to queue
    :param subjects: list
    :param user: User
    :param session: Session
    :return: Json
    """

    return adding_to_staging(subjects=subjects, user=user)


@matchmaking_router.delete('/api/matchmaking')
def staging_cancel(user: UserTable = Depends(get_current_user)):
    """ DELETE endpoint that deletes user from queue

    :param user: User
    :param session: Session
    :return: Json
    """

    return delete_from_staging(user=user)
