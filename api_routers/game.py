from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from models import add_to_game, leave_game, make_try
from store import User, get_session

game_router = APIRouter()


@game_router.post('/api/game')
def game_adding(user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return add_to_game(user=user, session=session)


@game_router.delete('/api/game/cancel')
def game_leaving(user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    return leave_game(user=user, session=session)


@game_router.post('/api/game/try')
def trying(answer: str, user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    return make_try(
        answer=answer, user=user, session=session
    )