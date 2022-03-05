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

    class Config:
        orm_mode = True


class UserUpdate(UserModel):

    class Config:
        orm_mode = True


class Token(BaseModel):
    """ Scheme of token

        fields:
        access_token: str
            jwt token
        token_type: str
            type of token
    """
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    """ Scheme of token with user's username
        fields:
        username: Optional[str]
    """
    username: Optional[str] = None

    class Config:
        orm_mode = True


class TaskModel(BaseModel):
    """Scheme of task
        fields:
        name: str
            task name
        subject: str
            task's subject
        content: str
            task's content
        right_answer: str
            task's right answer
        scores: float
            max scores for this task
    """
    name: str
    subject: str
    content: str
    right_answer: str
    scores: float

    class Config:
        orm_mode = True