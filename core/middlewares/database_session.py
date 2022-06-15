from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_protocol = 'sqlite:///core/store/database.db'
engine = create_engine(database_protocol)
session = sessionmaker(bind=engine)


def generate_session():
    sess = session()
    try:
        yield sess
    finally:
        sess.close()
