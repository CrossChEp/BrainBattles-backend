from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    nickname: Optional[str]
    email: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None