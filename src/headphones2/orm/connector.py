import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import headphones2

from .media import Base

DB_FILE = os.path.abspath(os.path.join(headphones2.__path__[0], '..', '..', 'headphones2.db'))


def connect():
    engine = create_engine('sqlite:///' + DB_FILE).connect()
    Session = sessionmaker(bind=engine)
    return Session()


def create_all_tables():
    Base.metadata.create_all(connect())
