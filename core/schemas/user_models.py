from datetime import datetime
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

    class Config:
        orm_mode = True


class UserGetModel(BaseUserModel):
    id: int
    organization: Optional[str]
    region: Optional[str]
    contacts: Optional[dict]
    rank: Optional[str]
    wins: Optional[int]
    scores: Optional[int]
    games: Optional[int]
    state: Optional[str]

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


class UserAbstractModel(UserUpdateModel):
    id: Optional[int]

    class Config:
        orm_mode = True


class BanUserModel(BaseModel):
    id: int
    term: Optional[datetime]

    class Config:
        orm_mode = True


class UserUpdateAdminModel(UserUpdateModel):
    rank: Optional[str]
    wins: Optional[int]
    scores: Optional[int]
    games: Optional[int]

    class Config:
        orm_mode = True
