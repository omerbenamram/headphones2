from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

CONFIGURATION_PATH = os.path.join(__file__, os.pardir, os.pardir, 'configuration.json')

LOSSY_MEDIA_FORMATS = ["mp3", "aac", "ogg", "ape", "m4a", "asf", "wma"]
LOSSLESS_MEDIA_FORMATS = ["flac"]
MEDIA_FORMATS = LOSSY_MEDIA_FORMATS + LOSSLESS_MEDIA_FORMATS
