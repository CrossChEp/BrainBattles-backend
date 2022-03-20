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
    id: Optional[int] = None

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
        rank: str
            rank of task
    """
    name: str
    subject: str
    content: str
    right_answer: str
    scores: float
    rank: str

    class Config:
        orm_mode = True


class QueueModel(BaseModel):
    user_id: int
    subject: str
    rank: str

    class Config:
        orm_mode = True


class GameModel(BaseModel):
    user_id: int
    opponent_id: int
    task: str

    class Config:
        orm_mode = True
