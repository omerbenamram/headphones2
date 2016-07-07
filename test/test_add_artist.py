from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import datetime
import os

import logbook
import musicbrainzngs
import pytest
from headphones2.orm import *
from headphones2.tasks import add_artist_to_db

from .fixtures import *
from .conftest import vcr

logger = logbook.Logger(__name__)

# if cassettes exist, turn off rate limiting
current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, 'fixtures', 'cassettes')):
    logger.info('Cassettes directory existsing, turning off rate-limiting')
    musicbrainzngs.set_rate_limit(False)
else:
    logger.warn("Couldn't find cassettes, going to hit real musicbrainz API")


@pytest.mark.parametrize("artist_id", [
    AYREON_MBID
])
@vcr.use_cassette(record_mode='new_episodes')
def test_add_artist_to_db(session, artist_id):
    artist_id = artist_id

    add_artist_to_db(artist_id, session)

    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()

    assert artist
    assert artist.name == 'Ayreon'
    assert artist.musicbrainz_id == artist_id

    toe_album = artist.albums.filter_by(title='The Theory of Everything').first()
    assert toe_album
    assert toe_album.musicbrainz_id == '6281bcfe-058e-4cd3-85bc-66f47c28960b'

    releases = session.query(Release).filter_by(album=toe_album)

    assert releases.count() == 7
    release = releases.filter_by(asin='B00F2HW220').first()
    assert release.tracks.count() == 42
    assert release.release_date == datetime.datetime(2013, 10, 25)
    assert releases.filter_by(is_selected=True).count() == 1


# Air has some different resulting dicts structure
def test_add_artist_type_2_to_db(session):
    artist_id = AIR_MBID

    add_artist_to_db(artist_id, session)

    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()

    assert artist
    assert artist.name == 'Air'


@vcr.use_cassette()
def test_delete_artist_from_db(session_with_artist):
    # add artist test case
    artist_id = AYREON_MBID
    session = session_with_artist

    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()

    session.delete(artist)
    session.commit()

    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()

    assert not artist
    albums = session.query(Album).join(Artist).filter(Artist.musicbrainz_id == artist_id)
    assert albums.count() == 0
