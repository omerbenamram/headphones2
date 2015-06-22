from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from pies.overrides import *
import logbook
import py

from beets.library import Item
from headphones2.config import MEDIA_FORMATS
from headphones2.postprocess import AcoustIDAlbumTagger, BeetsTagger, PostProcessorException, Renamer
from headphones2.postprocess.taggers.simple_tagger import BeetsTaggerException

logger = logbook.Logger(__name__)
Path = py.path.local


def _collect_files_from_folder(folder_path, wanted_formats=MEDIA_FORMATS):
    p = Path(folder_path)
    assert p.isdir(), "Got non directory input, breaking"

    media_files_paths = []

    # .mp3/mp3 --> .mp3
    extensions = map(lambda x: ".{}".format(x) if not x.startswith(".") else "*{}".format(x), wanted_formats)
    for ext in extensions:
        matches = p.listdir(fil=lambda x: x.ext == ext)
        media_files_paths.extend(map(str, matches))

    return media_files_paths


def post_process_folder(folder, expected_artist=None, expected_album=None, should_move=False,
                        flatten_result_folder=False):
    logger.info("Started post processing for {}".format(folder))
    logger.debug("Collecting media items from folders")

    media_files_paths = _collect_files_from_folder(folder, wanted_formats=MEDIA_FORMATS)
    items = [Item.from_path(str(f)) for f in media_files_paths]

    post_processors = []
    aid_tagger = AcoustIDAlbumTagger()
    beets_tagger = BeetsTagger()
    renamer = Renamer()

    for tagger in [aid_tagger, beets_tagger, renamer]:
        post_processors.append(tagger)

    try:
        beets_result = beets_tagger.process(items, expected_artist=expected_artist, expected_album=expected_album)
    except BeetsTaggerException:  # beets tagging flow failed
        logger.exception('Calling AcoustID Tagger')
        recommendation = aid_tagger.process(items)
        if recommendation:
            beets_result = beets_tagger.process(items, expected_artist=expected_artist,
                                                expected_album=expected_album,
                                                expected_release_id=recommendation)
        else:
            raise PostProcessorException("Exhasted tagging options, failing")

    renamer.process(items, flatten_folder=flatten_result_folder)

    _write_all_changes(items, list_of_post_processors=post_processors,
                       album_info=beets_result.album_info_object, track_mapping=beets_result.track_mapping_object)

    logger.info("Post processor compelted for {}".format(folder))


def _write_all_changes(list_of_items, list_of_post_processors=(), **kwargs):
    """
    :param list_of_items:
    :type list_of_items: list[beets.Library.Item]
    :param list_of_post_processors:
    :type list_of_post_processors: list[headphones2.postprocess.component_base.PostProcessor]
    :return:
    """
    logger.info("Writing changes to files")
    for post_processor in list_of_post_processors:
        post_processor.write(list_of_items, **kwargs)

    return True
