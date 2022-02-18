from tokenize import String

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

base = declarative_base()


class User(base):
    __tablenam__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String)