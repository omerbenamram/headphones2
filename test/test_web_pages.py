import pytest
from flask import Response
from bs4 import BeautifulSoup

from conftest import vcr

from headphones2.app import app as _app


@pytest.fixture
def app():
    app = _app
    app.response_class = Response
    return app


@vcr.use_cassette
def test_load_artist_page(client):
    artist_id = '7bbfd77c-1102-4831-9ba8-246fb67460b3'  # Ayreon.
    ayreon_albums = {u'01011001',
                     u'Actual Fantasy',
                     u'Ayreonauts Only',
                     u'Into the Electric Castle',
                     u'The Final Experiment',
                     u'The Human Equation',
                     u'The Theory of Everything',
                     u'Timeline',
                     u'Universal Migrator Part I & II',
                     u'Universal Migrator, Part 1: The Dream Sequencer',
                     u'Universal Migrator, Part 2: Flight of the Migrator'}
    res = client.get('/artistPage?ArtistID={}'.format(artist_id))
    bs = BeautifulSoup(res.get_data())
    assert res.status_code == 200
    # [1:] to ignore table head
    assert set([x.a.text for x in bs.findAll(attrs={'id': 'albumname'})[1:]]) == ayreon_albums

def test_load_bad_artist_page(client):
    artist_id = 'aaaaa-aaaaa-aaaa-aaaa-aaaaaaa'  # bad id.
    res = client.get('/artistPage?ArtistID={}'.format(artist_id))
    assert res.status_code == 404
