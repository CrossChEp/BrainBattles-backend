from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from store.user_methods import users_get, user_add, user_delete, get_user
from store.db_model import User
from store.auth_methods import authenticate_user


database_protocol = 'sqlite:///store/database.db'
engine = create_engine(database_protocol)
session = sessionmaker(bind=engine)


def get_session():
    sess = session()
    try:
        yield sess
    finally:
        sess.close()
