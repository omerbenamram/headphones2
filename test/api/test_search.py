import pytest
from flask import url_for

from headphones2.compat.http import HTTPStatus


@pytest.mark.parametrize("input_params, status_code", [
    ({'q': 'Symphony X'}, HTTPStatus.PRECONDITION_REQUIRED.value),
    ({'q': 'Symphony X', 'type': 'artist'}, HTTPStatus.OK.value),
    ({'type': 'artist'}, HTTPStatus.PRECONDITION_REQUIRED.value),
    ({'q': 'Symphony X', 'type': 'bleh'}, HTTPStatus.PRECONDITION_FAILED.value),
])
def test_search_returns_correct_http_codes(client, input_params, status_code):
    url = url_for('search.search_musicbrainz_for_artist', **input_params)
    res = client.get(url)
    assert res.status_code == status_code
