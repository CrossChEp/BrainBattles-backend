""" Module for database

    Classes:
        User
            users' table
        Task
            tasks' table
        Staging
            queue's table
        Game
            games' table

    Functions:
        get_session
            gets database session
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from store.db_model import User, Task, TaskModeration

database_protocol = 'sqlite:///store/database.db'
engine = create_engine(database_protocol)
session = sessionmaker(bind=engine)


def get_session():
    sess = session()
    try:
        yield sess
    finally:
        sess.close()
