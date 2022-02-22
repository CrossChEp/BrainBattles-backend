import bcrypt
from fastapi import Query
from sqlalchemy.orm import Session

from schemas import UserModel
from schemas.api_models import UserUpdate
from store.db_model import User


def users_get(session: Session):
    users = session.query(User).all()
    return users


def user_add(user: UserModel, session: Session):
    user.password = bcrypt.hashpw(
        user.password.encode(),
        salt=bcrypt.gensalt()
    )
    new_user = User(**user.dict())
    new_user.scores = 0
    session.add(new_user)
    session.commit()


def user_delete(id: int, session: Session):
    user = session.query(User).filter_by(id=id).first()
    session.delete(user)
    session.commit()


def get_user(user: UserModel, session: Session):
    new_user = {}
    for key, value in user.dict().items():
        if value is None:
            pass
        else:
            new_user[key] = value

    user = session.query(User).filter_by(**new_user).first()
    return user


def user_update(user: User, update_data: UserUpdate, session: Session):
    req: Query = session.query(User).filter_by(id=user.id)
    new_user = {}
    for key, value in update_data.dict().items():
        if value is None:
            pass
        if key == 'password':
            value = bcrypt.hashpw(
                value.encode(),
                bcrypt.gensalt()
            )
        new_user[key] = value
    req.update(new_user)
    session.commit()
