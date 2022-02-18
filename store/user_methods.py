import bcrypt
from sqlalchemy.orm import Session

from schemas import UserModel
from store.db_model import User


def users_get(session: Session):
    users = session.query(User).all()
    return users


def user_add(user: UserModel, session: Session):
    user.password = bcrypt.hashpw(
        user.password.encode(),
        salt=bcrypt.gensalt()
    )
    new_user = User(
        nickname=user.nickname,
        email=user.email,
        name=user.name,
        surname=user.surname,
        password=user.password
    )

    session.add(new_user)
    session.commit()


def user_delete(id: int, session: Session):
    user = session.query(User).filter_by(id=id).first()
    session.delete(user)
    session.commit()


def get_user(user: UserModel, session: Session):
    user = session.query(User).filter_by(**user.dict()).first()
    return user