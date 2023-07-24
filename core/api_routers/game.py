from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from core.api_routers.auth import get_current_user
from core.middlewares.database_session import generate_session
from core.models import add_to_game, leave_game, make_try, winner_check, connect_to_game
from core.models.websockets.game import GameConnectionManager
from core.store import UserTable

game_router = APIRouter()
connection_manager = GameConnectionManager()


@game_router.post('/api/game')
def game_adding(user: UserTable = Depends(get_current_user),
                session: Session = Depends(generate_session)):
    """ POST endpoint for adding user to game

    :param user: User
    :param session: Session
    :return: dict or HTTPException
    """

    return add_to_game(user=user, session=session)


@game_router.websocket('/api/websocket_game/{key_fraze}/{task_id}')
async def websocket_game(key_fraze: str, task_id: int,
                         websocket: WebSocket, token: str):
     # await connect_to_game(websocket, key_fraze, task_id, user, session)
    # pass
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)


@game_router.delete('/api/game/cancel')
def game_leaving(user: UserTable = Depends(get_current_user),
                 session: Session = Depends(generate_session)):
    """ DELETE endpoint for deleting user from game

    :param user: User
    :param session: Session
    :return: Json
    """

    return leave_game(user=user, session=session)


@game_router.post('/api/game/try')
def trying(answer: str, user: UserTable = Depends(get_current_user),
           session: Session = Depends(generate_session)):
    """ POST endpoint for making try

    :param answer: str
    :param user: User
    :param session: Session
    :return: None
    """

    return make_try(
        answer=answer, user=user, session=session
    )


@game_router.get('/api/game/winner')
def check_winner(user: UserTable = Depends(get_current_user)):
    return winner_check(user=user)
