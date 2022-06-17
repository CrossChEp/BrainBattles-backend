"""Module for users' database methods"""

from fastapi import Query, HTTPException
from sqlalchemy.orm import Session
from core.models.images.image_methods import create_default_image
from core.models.user.user_auxilary_methods import check_forbidden_nickname, check_avatar_availability, \
    hash_password, create_pfp, is_user_exists, generate_new_user, generate_user_get_model_for_many_users
from core.schemas import UserRegisterModel, UserUpdateModel, UserAbstractModel
from core.store.db_model import UserTable
from core.models.general_methods import model_without_nones


def users_get(session: Session):
    """
    gets all users from database
    :param session: Session
    :return: User
    """
    users = session.query(UserTable).all()
    user_models = generate_user_get_model_for_many_users(users)
    return user_models


def add_user_to_database(user: UserRegisterModel, session: Session) -> None:
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


def delete_user_from_database(user: UserTable, session: Session):
    """
    deletes user from database
    :param user: User
    :param session: Session
    :return: None
    """
    user = session.query(UserTable).filter_by(id=user.id).first()
    session.delete(user)
    session.commit()


def get_user_by_id(user_id: int, session: Session) -> UserTable:
    """ gets user by user id

    :param user_id: int
        (user id)
    :param session: Session
    :return: User
    """

    user = session.query(UserTable).filter_by(id=user_id).first()
    return user


def get_user(user: UserAbstractModel, session: Session):
    """
    gets concrete user
    :param user: UserModel
    :param session: Session
    :return: User
    """
    new_user = model_without_nones(user.dict())

    user = session.query(UserTable).filter_by(**new_user).first()
    return user


def update_user_data(user: UserTable, update_data: UserUpdateModel, session: Session):
    """
    updates user in database
    :param user: User
    :param update_data: UserUpdate
    :param session: Session
    :return: None
    """

    if update_data.nickname:
        is_user_exists(nickname=update_data.nickname, session=session)

    check_forbidden_nickname(nickname=update_data.nickname)

    req: Query = session.query(UserTable).filter_by(id=user.id)

    if update_data.password:
        update_data.password = hash_password(password=update_data.password)

    if update_data.avatar is not None:
        create_pfp(avatar=update_data.avatar, nickname=update_data.nickname)

    checked_user_data = model_without_nones(update_data.dict())
    req.update(checked_user_data)
    session.commit()
