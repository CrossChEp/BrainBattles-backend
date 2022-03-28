"""Module for users' database methods"""

from fastapi import Query, HTTPException
from sqlalchemy.orm import Session
from models.images.image_methods import create_default_image
from models.user.user_auxilary_methods import check_forbidden_nickname, check_avatar_availability, \
    hash_password, create_pfp, is_user_exists, generate_new_user
from schemas import UserModel, UserUpdate
from store.db_model import User


def users_get(session: Session):
    """
    gets all users from database
    :param session: Session
    :return: User
    """
    users = session.query(User).all()
    return users


def user_add(user: UserModel, session: Session) -> None:
    """
    adds user to database
    :param user: UserModel
    :param session: Session
    :return: None
    """
    user.password = hash_password(password=user.password)

    avatar = create_default_image()
    create_pfp(avatar=avatar, nickname=user.nickname)

    is_user_exists(nickname=user.nickname, session=session)

    generate_new_user(user_model=user, session=session)


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
    """ gets user by user id

    :param uid: int
        (user id)
    :param session: Session
    :return: User
    """

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

    if update_data.nickname:
        is_nickname_exists = session.query(User).filter_by(nickname=update_data.nickname).all()
        if is_nickname_exists:
            raise HTTPException(status_code=403, detail='user with such nickname already exists')

    check_forbidden_nickname(nickname=update_data.nickname)

    req: Query = session.query(User).filter_by(id=user.id)
    checked_user_data = check_avatar_availability(user_update_data=update_data)

    if update_data.password:
        checked_user_data.password = hash_password(password=checked_user_data.password)
    req.update(checked_user_data.dict())

    if update_data.avatar is not None:
        create_pfp(avatar=update_data.avatar, nickname=checked_user_data.nickname)
    session.commit()
