import bcrypt
from fastapi import HTTPException

from schemas import UserUpdate, UserModel

FORBIDDEN_NICKNAMES = [
    'con'
]


def generate_user_model(user_json: dict) -> UserModel:
    return UserModel(**user_json)


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


def check_avatar_availability(user_update_data: UserUpdate):
    """ returns json without avatar if avatar
    doesn't exist or output json


    :param user_update_data: UserUpdate
        (user's update data)
    :return: dict
    """
    if user_update_data.avatar is None:
        user_dict = skip_json_key(json=user_update_data.dict(), key='avatar')
        return generate_user_model(user_json=user_dict)
    return user_update_data


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

