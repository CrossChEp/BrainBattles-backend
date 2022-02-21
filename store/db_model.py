from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    tasks = relationship('Task', backref='user')
    staging = relationship('Staging', backref='user')

class Task(base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    content = Column(String)
    right_answer = Column(String)
    author = Column(Integer, ForeignKey('users.id'))


class Staging(base):
    __tablename__ = 'staging'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))