import pytest
from flask import url_for

from headphones2.compat.http import HTTPStatus

SAMPLE_GOOD_CONFIGURATION = {
    'libraryPath': r'\\penny\Music',
    'debug': 'false'
}


@pytest.mark.parametrize("input_params, status_code", [
    (SAMPLE_GOOD_CONFIGURATION, HTTPStatus.OK.value),
])
def test_search_returns_correct_http_codes(client, input_params, status_code):
    url = url_for('configuration_api.update_configuration', **input_params)
    res = client.get(url)
    assert res.status_code == status_code


def test_configuration_loads_successfully(client):
    url = url_for('configuration_api.update_configuration')
    res = client.get(url)
    assert res.status_code == HTTPStatus.OK.value
