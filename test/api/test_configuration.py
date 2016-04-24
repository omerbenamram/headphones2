import pytest
from flask import url_for

from headphones2.compat.http import HTTPStatus


@pytest.mark.parametrize("input_params, status_code", [
    ({'q': 'Symphony X'}, HTTPStatus.BAD_REQUEST.value),
    ({'q': 'Symphony X', 'type': 'artist'}, HTTPStatus.OK.value),

    ({'q': 'The Divine Wings of Tragedy', 'type': 'release'}, HTTPStatus.OK.value),
    ({'q': 'Symphony X', 'type': 'bleh'}, HTTPStatus.BAD_REQUEST.value),
])
def test_search_returns_correct_http_codes(client, input_params, status_code):
    url = url_for('search.update_configuration', **input_params)
    res = client.get(url)
    assert res.status_code == status_code
