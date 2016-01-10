from __future__ import (absolute_import, division, print_function, unicode_literals)

from contextlib import closing

from .engine import huey
from ..importer import add_artist_to_db
from ..orm import connect


@huey.task()
def add_artist_task(artist_id):
    with closing(connect()) as session:
        add_artist_to_db(artist_id, session)
