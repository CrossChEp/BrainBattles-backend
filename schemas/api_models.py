from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    nickname: str
    email: str
    name: str
    surname: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None