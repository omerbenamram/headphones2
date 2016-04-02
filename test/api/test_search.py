import pytest
from flask import url_for
from ..conftest import vcr

from headphones2.compat.http import HTTPStatus


# TODO: check 500 errors?
@pytest.mark.parametrize("input_params, status_code", [
    ({'q': 'Symphony X'}, HTTPStatus.PRECONDITION_REQUIRED.value),
    ({'q': 'Symphony X', 'type': 'artist'}, HTTPStatus.OK.value),
    ({'type': 'artist'}, HTTPStatus.PRECONDITION_REQUIRED.value),
    ({'type': 'release'}, HTTPStatus.PRECONDITION_REQUIRED.value),
    ({'q': 'The Divine Wings of Tragedy', 'type': 'release'}, HTTPStatus.OK.value),
    ({'q': 'Symphony X', 'type': 'bleh'}, HTTPStatus.PRECONDITION_FAILED.value),
])
def test_search_returns_correct_http_codes(client, input_params, status_code):
    url = url_for('search.search_musicbrainz', **input_params)
    with vcr.use_cassette('test_search', record_mode='new_episodes'):
        res = client.get(url)
    assert res.status_code == status_code
