from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.api_routers.auth import get_current_user
from core.controllers import get_all_users_controller, delete_user_controller
from core.middlewares.database_session import generate_session
from core.models import users_get, add_user_to_database, delete_user_from_database, update_user_data, get_user_by_id
from core.schemas import UserGetModel, UserRegisterModel, UserUpdateModel
from core.store import UserTable

users_router = APIRouter()


@users_router.get('/api/users')
def get_all_users(user: UserTable = Depends(get_current_user)) -> List[UserGetModel]:
    """ GET endpoint that gets all users from database

    :param session: Session
    :return: Json
    """

    return get_all_users_controller(user)


@users_router.post('/api/register')
def register_user(user: UserRegisterModel, session: Session = Depends(generate_session)):
    """ POST endpoint that adds user to database

    :param user: UserModel
    :param session: Session
    :return: None
    """

    return add_user_to_database(user=user, session=session)


@users_router.delete('/api/users')
def delete_user(user: UserTable = Depends(get_current_user)):
    """ DELETE endpoint that deletes user from database

    :param user: User
    :return: None
    """

    return delete_user_controller(user)


@users_router.put('/api/users')
def update_user(update_data: UserUpdateModel, user: UserTable = Depends(get_current_user),
                session: Session = Depends(generate_session)):
    """PUT endpoint that updates user's data

    :param update_data: UserUpdate
    :param user: User
    :param session: Session
    :return: None
    """

    return update_user_data(user=user, session=session, update_data=update_data)


@users_router.get('/api/user/{user_id}')
def get_user(user_id: int, session: Session = Depends(generate_session)):
    return get_user_by_id(user_id=user_id, session=session)
