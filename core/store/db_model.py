from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()


class UserTable(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    organization = Column(String)
    region = Column(String)
    contacts = Column(JSON)
    scores = Column(Float)
    rank = Column(String)
    wins = Column(Integer)
    games = Column(Integer)
    state = Column(String)
    tasks = relationship('TaskTable', backref='user')


class TaskTable(base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    content = Column(String)
    right_answer = Column(String)
    scores = Column(Float)
    rank = Column(String)
    author = Column(Integer, ForeignKey('users.id'))
    is_moderated = relationship('TaskModerationTable', backref='task', cascade='all, delete')


class TaskModerationTable(base):
    __tablename__ = 'tasks_moderation'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
