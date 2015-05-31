import os
import vcr as _vcr

CASSETTE_LIBRARY_DIR = os.path.join(__file__, '..', 'fixtures', 'cassettes')
vcr = _vcr.VCR(cassette_library_dir=CASSETTE_LIBRARY_DIR)


