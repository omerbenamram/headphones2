from sqlalchemy import create_engine

from .media import Base


def connect():
    return create_engine('sqlite:///C:\\git\\headphones-reloaded\\headphones2.db').connect()

def create_all_tables():
    Base.metadata.create_all(connect())
