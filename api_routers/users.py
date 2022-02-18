from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from schemas import UserModel
from schemas.api_models import UserUpdate
from store import users_get, get_session, user_add, user_delete, user_update, User

users_router = APIRouter()


@users_router.get('/users')
def get_users(session: Session = Depends(get_session)):
    return users_get(session=session)


@users_router.post('/register')
def add_user(user: UserModel, session: Session = Depends(get_session)):
    return user_add(user=user, session=session)


@users_router.delete('/users')
def delete_user(id: int, session: Session = Depends(get_session)):
    return user_delete(id=id, session=session)


@users_router.put('/users')
def update_user(update_data: UserUpdate, user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return user_update(user=user, session=session, update_data=update_data)