from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from models import add_to_game
from store import User, get_session

game_router = APIRouter()


@game_router.post('/api/game')
def game_adding(user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return add_to_game(user=user, session=session)