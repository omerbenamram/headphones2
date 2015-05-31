import pytest
from flask import Response

from headphones2.app import app as _app


@pytest.fixture
def app():
    app = _app
    app.response_class = Response
    return app


def test_load_artist_page(client):
    artist_id = '7bbfd77c-1102-4831-9ba8-246fb67460b3'  # Ayreon.
    res = client.get('/artistPage?ArtistID={}'.format(artist_id))
    assert res.status_code == 200


def test_load_bad_artist_page(client):
    artist_id = 'aaaaa-aaaaa-aaaa-aaaa-aaaaaaa'  # bad id.
    res = client.get('/artistPage?ArtistID={}'.format(artist_id))
    assert res.status_code == 404
