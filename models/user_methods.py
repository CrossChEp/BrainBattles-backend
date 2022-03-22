import base64

import bcrypt
from fastapi import Query, HTTPException
from sqlalchemy.orm import Session

from configs import ranks
from models.image_methods import decode_image
from schemas import UserModel, UserGetModel, UserUpdate
from store.db_model import User


def users_get(session: Session):
    """
    gets all users from database
    :param session: Session
    :return: User
    """
    users = session.query(User).all()
    return users


def user_add(user: UserModel, session: Session):
    """
    adds user to database
    :param user: UserModel
    :param session: Session
    :return: None
    """
    user.password = bcrypt.hashpw(
        user.password.encode(),
        salt=bcrypt.gensalt()
    )
    with open('store/user_image.jpeg', 'rb') as image:
        avatar = base64.encodebytes(image.read()).hex()
    with open(f'static/{user.nickname}.jpeg', 'wb') as pfp:
        image = decode_image(avatar)
        pfp.write(image)
    new_user = User(**user.dict())
    new_user.scores = 0
    new_user.rank = ranks[new_user.scores]
    session.add(new_user)
    session.commit()


def user_delete(user: User, session: Session):
    """
    deletes user from database
    :param user: User
    :param session: Session
    :return: None
    """
    user = session.query(User).filter_by(id=user.id).first()
    session.delete(user)
    session.commit()


def get_user_by_id(uid: int, session: Session) -> User:
    user = session.query(User).filter_by(id=uid).first()
    return user


def get_user(user: UserModel, session: Session):
    """
    gets concrete user
    :param user: UserModel
    :param session: Session
    :return: User
    """
    new_user = {}
    for key, value in user.dict().items():
        if value is None:
            pass
        else:
            new_user[key] = value

    user = session.query(User).filter_by(**new_user).first()
    return user


def user_update(user: User, update_data: UserUpdate, session: Session):
    """
    updates user in database
    :param user: User
    :param update_data: UserUpdate
    :param session: Session
    :return: None
    """
    try:
        if user.nickname.lower() == 'con':
            raise HTTPException(status_code=406, detail='user with nickname "con" are not allowed')
    except AttributeError:
        pass

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
    if update_data.avatar is not None:
        with open(f'/static/{req.first().nickname}.jpeg', 'wb') as img:
            pfp = decode_image(user.avatar)
            img.write(pfp)
    session.commit()
