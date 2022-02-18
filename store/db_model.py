
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

base = declarative_base()


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String)