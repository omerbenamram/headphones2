from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os

from pies.overrides import *

import logbook
import py
import tempfile

from beets.library import Item
from headphones2.config import MEDIA_FORMATS
from headphones2.postprocess import AcoustIDAlbumTagger, BeetsTagger, Renamer, AlbumTask

logger = logbook.Logger(__name__)
Path = py.path.local

def pre_process_folder(folder):
    p = Path(folder)
    assert p.isdir(), "Got non directory input, breaking"

    paths = _collect_files_from_folder(p)
    items = [Item.from_path(str(f)) for f in paths]
    tempdir = tempfile.mkdtemp(prefix='temp_')
    for item in items:
        filename = os.path.basename(item.path)
        item.move_file(os.path.join(tempdir, filename), copy=True)
    yield AlbumTask(items)


def _collect_files_from_folder(folder, wanted_formats=MEDIA_FORMATS):
    """
    :param folder: folder path object
    :type folder: py.path.local
    :param wanted_formats:
    :return: list of files
    """
    media_files_paths = []

    # .mp3/mp3 --> .mp3
    extensions = map(lambda x: ".{}".format(x) if not x.startswith(".") else "*{}".format(x), wanted_formats)
    for ext in extensions:
        matches = folder.listdir(fil=lambda x: x.ext == ext)
        media_files_paths.extend(map(str, matches))

    return media_files_paths


def post_process_album_task(task, expected_artist=None, expected_album=None, should_move=False,
                            flatten_result_folder=False, destination_folder=str(Path(os.path.expanduser("~")).join("Music"))):
    """

    :param task: the task object to process
    :type task: AlbumTask
    :param expected_artist: the artist name (optional)
    :param expected_album: the album name (optional)
    :param should_move:
    :param flatten_result_folder:
    :return:
    """
    logger.info("Started post processing for {}".format(task))

    aid_tagger = AcoustIDAlbumTagger()
    beets_tagger = BeetsTagger()
    renamer = Renamer()

    beets_tagger.process(task, expected_artist=expected_artist, expected_album=expected_album,
                         fallback_taggers=[aid_tagger])

    task.write_metadata_changes()
    renamer.process(task, destination_folder=destination_folder, flatten_folder=flatten_result_folder)

    task.write_to_disk(should_move=should_move)

    logger.info("Post processor compelted for {}".format(task))
