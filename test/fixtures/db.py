from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import pickle as pkl

import pytest
from beets.library import Item
from headphones2.orm import connect
from headphones2.orm.connector import create_all_tables
from headphones2.tasks import add_artist_to_db

from test.conftest import vcr
from test.fixtures.ids import AYREON_MBID

__all__ = ['session', 'session_with_artist', 'folder_info']


# noinspection PyShadowingNames
@pytest.yield_fixture()
def session(tmpdir):
    db_file = os.path.join(tmpdir.strpath, 'temp.db')
    if os.path.exists(db_file):
        os.remove(db_file)

    create_all_tables(db_file)
    session = connect(db_file)
    yield session
    session.close()


# noinspection PyShadowingNames
@pytest.yield_fixture()
def session_with_artist(tmpdir):
    db_file = os.path.join(tmpdir.strpath, 'temp.db')
    if os.path.exists(db_file):
        os.remove(db_file)

    create_all_tables(db_file)
    session = connect(db_file)
    with vcr.use_cassette('test_add_artist_to_db'):
        add_artist_to_db(AYREON_MBID, session)  # Tested separately
    session.commit()
    yield session
    session.close()


@pytest.fixture()
def folder_info():
    """
    Album info, track->items mapping pickle
    :return:
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'universal_migrator.pkl')
    with open(path) as f:
        return pkl.load(f)
