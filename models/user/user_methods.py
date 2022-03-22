import base64

import bcrypt
from fastapi import Query, HTTPException
from sqlalchemy.orm import Session

from configs import ranks
from models.image_methods import decode_image
from models.user.user_auxilary_methods import check_forbidden_nickname, skip_json_key, check_avatar_availability, \
    hash_password
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
    check_forbidden_nickname(nickname=update_data.nickname)

    req: Query = session.query(User).filter_by(id=user.id)
    checked_user_data = check_avatar_availability(user_update_data=update_data)

    if update_data.password:
        checked_user_data.password = hash_password(password=checked_user_data.password)
    req.update(checked_user_data.dict())

    if update_data.avatar is not None:
        with open(f'/static/{req.first().nickname}.jpeg', 'wb') as img:
            pfp = decode_image(update_data.avatar)
            img.write(pfp)

    session.commit()
