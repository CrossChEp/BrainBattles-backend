"""Module for methods that used in user_methods module"""
from typing import List

import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs import ranks, DEFAULT
from core.models.images.image_methods import decode_image
from core.schemas import UserGetModel, UserRegisterModel, UserUpdateModel
from core.store import UserTable

FORBIDDEN_NICKNAMES = [
    'con'
]


# def generate_user_model(user_json: dict) -> UserModel:
#     """ generates user's model `UserModel` using user's json
#
#     :param user_json: dict
#         (user's json)
#     :return: UserModel
#     """
#     return UserModel(**user_json)


def generate_user_get_model_for_many_users(users: List[UserTable]) -> List[UserGetModel]:
    user_get_models = []
    for user in users:
        user_get_model = generate_user_get_model(user)
        user_get_models.append(user_get_model)
    return user_get_models


def generate_user_get_model(user: UserTable) -> UserGetModel:
    user_get_model = UserGetModel(
        id=user.id,
        nickname=user.nickname,
        email=user.email,
        name=user.name,
        surname=user.surname,
        organization=user.organization,
        region=user.region,
        contacts=user.contacts,
        rank=user.rank,
        wins=user.wins,
        scores=user.scores,
        games=user.games,
        state=user.state
    )
    return user_get_model


def check_forbidden_nickname(nickname: str):
    """ checks if user allowed to have
    such a nickname

    :param nickname: str
        (user's new nickname)
    """

    try:
        if nickname.lower() in FORBIDDEN_NICKNAMES:
            raise HTTPException(status_code=406, detail='user with such nickname are not allowed')
    except AttributeError:
        pass


def check_avatar_availability(user_update_data: UserUpdateModel):
    """ returns json without avatar if avatar
    doesn't exist or output json


    :param user_update_data: UserUpdate
        (user's update data)
    :return: dict
    """
    if user_update_data.avatar is None:
        user_dict = skip_json_key(json=user_update_data.dict(), key='avatar')
        return user_dict
    return user_update_data.dict()


def skip_json_key(json: dict, key) -> dict:
    """ Deletes key from json
    :param json: dict
    :param key:
        (key)
    :return: dict
    """
    json.pop(key)
    return json


def hash_password(password: str):
    """ hashes password


    :param password: str
        (input password)
    :return: bytes
        (hashed password)
    """
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )
    return hashed_password


def create_pfp(avatar, nickname: str) -> None:
    """ creates pfp to user
    :param avatar: str
        (user's future avatar)
    :param nickname: str
        (user's nickname)
    :return: None
    """
    with open(f'static/{nickname}.jpeg', 'wb') as img:
        pfp = decode_image(avatar)
        img.write(pfp)


def is_user_exists(nickname: str, session: Session):
    """checks if user with such nickname exists

    :param nickname: str
        (user nickname)
    :param session: Session
    """

    user = session.query(UserTable).filter_by(nickname=nickname).all()
    if user:
        raise HTTPException(status_code=403, detail='user with such nickname already exists')


def generate_new_user(user_model: UserRegisterModel, session: Session) -> None:
    """generates new user and adds him to database

    :param user_model: UserRegisterModel
        (user's model)
    :param session: Session
    :return: None
    """
    user_clear_model = skip_json_key(user_model.dict(), 'avatar')
    new_user = UserTable(**user_clear_model)
    new_user.scores = 0
    new_user.rank = ranks[new_user.scores]
    new_user.wins = 0
    new_user.games = 0
    new_user.state = DEFAULT
    session.add(new_user)
    session.commit()
