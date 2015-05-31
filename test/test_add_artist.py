import datetime
import os
import pytest
import vcr
from headphones2.importer import add_artist_to_db
from headphones2.orm import *
from headphones2.orm.connector import create_all_tables, DB_FILE
from headphones2.utils import musicbrainzngs
musicbrainzngs.set_rate_limit(False)


@pytest.yield_fixture()
def session(tmpdir):
    db_file = os.path.join(tmpdir.strpath, 'temp.db')
    if os.path.exists(db_file):
        os.remove(db_file)
    create_all_tables(db_file)
    session = connect(db_file)
    yield session
    session.close()


@vcr.use_cassette('fixtures/vcr_cassettes/test_add_artist_to_db_ayreon.yaml', record_mode='once')
def test_add_artist_to_db(session):
    artist_id = '7bbfd77c-1102-4831-9ba8-246fb67460b3'  # Ayreon.

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
    assert len(release.tracks) == 42
    assert release.release_date == datetime.datetime(2013, 10, 25)

if __name__ == '__main__':
    import py.path
    import tempfile
    tmpdir = py.path.local(tempfile.mkdtemp())
    s = session(tmpdir).next()
    test_add_artist_to_db(s)
    s.close()