from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    nickname: Optional[str]
    email: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True


class UserUpdate(UserModel):

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        orm_mode = True


class TaskModel(BaseModel):
    task_name: str
    subject: str
    content: str
    right_answer: str
    scores: float

    class Config:
        orm_mode = True