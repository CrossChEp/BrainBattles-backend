from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from schemas import UserModel
from schemas.api_models import UserUpdate
from models import users_get, user_add, user_delete, user_update
from store import get_session, User

users_router = APIRouter()


@users_router.get('/api/users')
def get_users(session: Session = Depends(get_session)):
    """ GET endpoint that gets all users from database

    :param session: Session
    :return: Json
    """

    return users_get(session=session)


@users_router.post('/api/register')
def add_user(user: UserModel, session: Session = Depends(get_session)):
    """ POST endpoint that adds user to database

    :param user: UserModel
    :param session: Session
    :return: None
    """

    return user_add(user=user, session=session)


@users_router.delete('/api/users')
def delete_user(id: int, session: Session = Depends(get_session)):
    """ DELETE endpoint that deletes user from database

    :param id: int
    :param session: Session
    :return: None
    """

    return user_delete(id=id, session=session)


@users_router.put('/api/users')
def update_user(update_data: UserUpdate, user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    """PUT endpoint that updates user's data

    :param update_data: UserUpdate
    :param user: User
    :param session: Session
    :return: None
    """

    return user_update(user=user, session=session, update_data=update_data)