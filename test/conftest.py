import pytest
import os
import vcr as _vcr
from headphones2.app import create_app

CASSETTE_LIBRARY_DIR = os.path.join(__file__, '..', 'fixtures', 'cassettes')
vcr = _vcr.VCR(cassette_library_dir=CASSETTE_LIBRARY_DIR)


# this is here for pytest-flask
@pytest.fixture
def app():
    app_fixture = create_app()
    return app_fixture
