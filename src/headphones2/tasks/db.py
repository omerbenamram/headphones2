from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from pies.overrides import *

from contextlib import closing
from ..orm import connect
from ..importer import add_artist_to_db
from .engine import huey


@huey.task()
def add_artist_task(artist_id):
    with closing(connect()) as session:
        add_artist_to_db(artist_id, session)
