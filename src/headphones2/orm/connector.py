import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import headphones2

from .media import Base

DB_FILE = os.path.abspath(os.path.join(headphones2.__path__[0], '..', '..', 'headphones2.db'))


def _create_engine():
    engine = create_engine('sqlite:///' + DB_FILE).connect()
    return engine


def connect():
    engine = _create_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def create_all_tables():
    engine = _create_engine()
    Base.metadata.create_all(engine)
