from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    """ Scheme of user

        fields:
        nickname: str
            user's nickname
        email: str
            user's email
        name: str
            user's name
        surname: str
            user's surname
        password: str
            user's password
    """
    nickname: Optional[str]
    email: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class UserGetModel(UserModel):
    id: int
    scores: int
    rank: str

    class Config:
        orm_mode = True


class UserUpdate(UserModel):
    avatar: Optional[str]

    class Config:
        orm_mode = True
