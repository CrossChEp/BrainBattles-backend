from pydantic import BaseModel


class UserModel(BaseModel):
    nickname: str
    email: str
    name: str
    surname: str
    password: str