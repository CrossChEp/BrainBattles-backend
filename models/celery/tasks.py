from sqlalchemy.orm import Session

from .celerys import app
from models import add_to_game
from store import User


@app.task(time_limit=3)
def add_user_to_game(user: User, session: Session):
    add_to_game(user=user, session=session)