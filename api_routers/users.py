from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserModel
from store import users_get, get_session, user_add

users_router = APIRouter()


@users_router.get('/users')
def get_users(session: Session = Depends(get_session)):
    return users_get(session=session)


@users_router.post('/register')
def add_user(user: UserModel, session: Session = Depends(get_session)):
    return user_add(user=user, session=session)