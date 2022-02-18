from sqlalchemy.orm import Session

from store.db_model import User


def users_get(session: Session):
    users = session.query(User).all()
    return users