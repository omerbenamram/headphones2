import datetime
import os

import pytest
import musicbrainzngs

from headphones2.importer import add_artist_to_db
from headphones2.orm import *
from headphones2.orm.connector import create_all_tables
from conftest import vcr

musicbrainzngs.set_rate_limit(False)

AYREON_MBID = '7bbfd77c-1102-4831-9ba8-246fb67460b3'  # Ayreon.


@pytest.yield_fixture()
def session(tmpdir):
    db_file = os.path.join(tmpdir.strpath, 'temp.db')
    if os.path.exists(db_file):
        os.remove(db_file)

    create_all_tables(db_file)
    session = connect(db_file)
    yield session
    session.close()

# TODO: NOT WORKING (VCR)
@vcr.use_cassette()
@pytest.yield_fixture()
def session_with_artist(tmpdir):
    db_file = os.path.join(tmpdir.strpath, 'temp.db')
    if os.path.exists(db_file):
        os.remove(db_file)

    create_all_tables(db_file)
    session = connect(db_file)
    add_artist_to_db(AYREON_MBID, session)  # Tested separately
    session.commit()
    yield session
    session.close()


@vcr.use_cassette()
def test_add_artist_to_db(session):
    artist_id = AYREON_MBID

    add_artist_to_db(artist_id, session)

    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()

    assert artist
    assert artist.name == 'Ayreon'
    assert artist.musicbrainz_id == artist_id

    toe_album = artist.albums.filter_by(title='The Theory of Everything').first()
    assert toe_album
    assert toe_album.musicbrainz_id == '6281bcfe-058e-4cd3-85bc-66f47c28960b'

    releases = session.query(Release).filter_by(album=toe_album)

    assert releases.count() == 5
    release = releases.filter_by(asin='B00F2HW220').first()
    assert release.tracks.count() == 42
    assert release.release_date == datetime.datetime(2013, 10, 25)
    assert releases.filter_by(is_selected=True).count() == 1


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
