import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import headphones2

from .media import Base

DB_FILE = os.path.abspath(os.path.join(headphones2.__path__[0], '..', '..', 'headphones2.db'))


def _create_engine(db_file):
    engine = create_engine('sqlite:///' + db_file).connect()
    return engine


def connect(db_file=DB_FILE):
    engine = _create_engine(db_file)
    Session = sessionmaker(bind=engine)
    return Session()


def create_all_tables(db_file=DB_FILE):
    engine = _create_engine(db_file)
    Base.metadata.create_all(engine)

    return engine
