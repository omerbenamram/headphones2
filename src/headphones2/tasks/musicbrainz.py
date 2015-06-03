from headphones2.external.musicbrainz import get_artwork_for_album
from . import huey


@huey.task()
def get_artwork_for_album_task(rgid):
    return get_artwork_for_album(rgid)
