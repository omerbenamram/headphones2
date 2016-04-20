from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from headphones2.external.musicbrainz import get_artwork_for_album
from . import huey


@huey.task(retries=3, retry_delay=5)
def get_artwork_for_album_task(rgid):
    return get_artwork_for_album(rgid)
