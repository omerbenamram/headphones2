from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook
import musicbrainzngs
import pytest
import os
import vcr as _vcr
from headphones2.app import create_app

__all__ = ['app', 'CASSETTE_LIBRARY_DIR', 'vcr', 'turn_off_musicbrainz_rate_limiting_if_cassette_exists']

CASSETTE_LIBRARY_DIR = os.path.abspath(os.path.join(__file__, '..', 'fixtures', 'cassettes'))
vcr = _vcr.VCR(cassette_library_dir=CASSETTE_LIBRARY_DIR)
logger = logbook.Logger(__name__)


def turn_off_musicbrainz_rate_limiting_if_cassette_exists(cassette_name):
    # if cassettes exist, turn off rate limiting
    cassette = os.path.join(CASSETTE_LIBRARY_DIR, cassette_name)
    if os.path.exists(cassette):
        logger.info('Cassettes directory existsing, turning off rate-limiting')
        musicbrainzngs.set_rate_limit(False)
    else:
        musicbrainzngs.set_rate_limit()
        logger.warn("Couldn't find cassettes, going to hit real musicbrainz API")


# this is here for pytest-flask
@pytest.fixture
def app():
    app_fixture = create_app()
    return app_fixture
