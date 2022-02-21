from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from models import adding_to_staging, delete_from_staging
from store import User, get_session

matchmaking_router = APIRouter()


@matchmaking_router.post('/matchmaking')
def add_to_staging(user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    return adding_to_staging(user=user, session=session)


@matchmaking_router.delete('/matchmaking')
def staging_cancel(user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    return delete_from_staging(user=user, session=session)