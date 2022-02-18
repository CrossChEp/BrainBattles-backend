from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from store import users_get, get_session

users_router = APIRouter()


@users_router.get('/users')
def get_users(session: Session = Depends(get_session)):
    return users_get(session=session)