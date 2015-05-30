from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .media import Base


def connect():
    engine = create_engine('sqlite:///C:\\git\\headphones-reloaded\\headphones2.db').connect()
    Session = sessionmaker(bind=engine)
    return Session()

def create_all_tables():
    Base.metadata.create_all(connect())
