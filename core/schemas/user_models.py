from typing import Optional

from pydantic import BaseModel


class BaseUserModel(BaseModel):
    nickname: str
    email: str
    name: Optional[str]
    surname: Optional[str]

    class Config:
        orm_mode = True


class UserRegisterModel(BaseUserModel):
    password: str
    avatar: Optional[str]


class UserGetModel(BaseUserModel):
    id: int
    organization: Optional[str]
    region: Optional[str]
    contacts: Optional[dict]
    rank: Optional[str]
    wins: Optional[int]
    scores: Optional[int]
    games: Optional[int]


class UserUpdateModel(BaseModel):
    nickname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    organization: Optional[str]
    region: Optional[str]
    contacts: Optional[str]
    avatar: Optional[str]


class UserAbstractModel(UserUpdateModel):
    id: Optional[int]

