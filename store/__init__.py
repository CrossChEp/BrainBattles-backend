from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from store.user_methods import users_get
from store.db_model import User


database_protocol = 'sqlite:///store/database.db'
engine = create_engine(database_protocol)
session = sessionmaker(bind=engine)


def get_session():
    sess = session()
    try:
        yield sess
    finally:
        sess.close()
