from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from pies.overrides import *

import logbook
import py

from beets.library import Item
from headphones2.config import MEDIA_FORMATS
from headphones2.postprocess import AcoustIDAlbumTagger, SimpleBeetsTagger, PostProcessorException, Renamer

logger = logbook.Logger()
Path = py.path.local


def _tag_album_and_fix_metadata(list_of_items, expected_artist=None, expected_album=None):
    aid_tagger = AcoustIDAlbumTagger()
    beets_tagger = SimpleBeetsTagger()
    try:
        beets_tagger.process(list_of_items, expected_artist=expected_artist, expected_album=expected_album)
    except PostProcessorException:  # simple tagging flow failed
        logger.exception('Calling AcoustID Tagger')
        is_success, recommendation = aid_tagger.process(list_of_items)
        if is_success:
            beets_tagger.process(list_of_items, expected_artist=expected_artist, expected_album=expected_album,
                                 expected_release_id=recommendation)
            return True
        raise PostProcessorException("Exhasted tagging options, failing")

    return True


def post_process_folder(folder, expected_artist=None, expected_album=None, should_move=False):
    logger.info("Started post processing for {}".format(folder))
    logger.debug("Collecting media items from folders")

    p = Path(folder)
    assert p.isdir(), "Got non directory input for postprocessor, breaking"

    file_pathes_to_process = []

    # .mp3/mp3 --> .mp3
    extensions = map(lambda x: ".{}".format(x) if not x.startswith(".") else "*{}".format(x), MEDIA_FORMATS)
    for ext in extensions:
        matches = p.listdir(fil=lambda x: x.ext == ext)
        file_pathes_to_process.extend(map(str, matches))

    items = [Item.from_path(str(f)) for f in file_pathes_to_process]

    _tag_album_and_fix_metadata(items, expected_artist=expected_artist, expected_album=expected_album)

    Renamer().process(items, should_move=should_move)

    logger.info("Post processor compelted for {}".format(folder))
