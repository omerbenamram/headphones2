from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
import uuid

from pies.overrides import *
import logbook
import py

from beets.autotag import apply_metadata
from beets.library import Item
from headphones2.config import MEDIA_FORMATS
from headphones2.postprocess import AcoustIDAlbumTagger, BeetsTagger, Renamer

logger = logbook.Logger(__name__)
Path = py.path.local


class AlbumTask(object):
    def __init__(self, list_of_items):
        self._item_list = list_of_items
        self._album_info_object = None
        self._track_mapping_object = None
        self._id = uuid.uuid4()
        self._path_mapping = {}

    @property
    def id(self):
        return self._id

    @property
    def items(self):
        return self._item_list

    def __iter__(self):
        for item in self._item_list:
            yield item

    def set_path_for_item(self, item, new_path):
        assert isinstance(new_path, str), "Path must be a string!"
        self._path_mapping[item.path] = new_path

    @property
    def is_completed(self):
        return all(map(lambda x: x is not None, [self._album_info_object, self._track_mapping_object]))

    def write_metadata_changes(self):
        assert self.is_completed, "Processing is not finished for task {}".format(self.id)
        apply_metadata(self._album_info_object, self._track_mapping_object)

        for item in self._item_list:
            item.write()

    def write_to_disk(self, should_move):
        # beets use "should copy"..
        copy = not should_move

        for item in self._item_list:
            destination_path = self._path_mapping[item.path]
            if not os.path.exists(os.path.dirname(destination_path)):
                os.makedirs(os.path.dirname(destination_path))

            item.move_file(destination_path, copy=copy)
            logger.info("{action} {orig} --> {new}".format(action=("Moving" if should_move else "Copying"),
                                                           orig=item.path, new=destination_path))


def pre_process_folder(folder):
    p = Path(folder)
    assert p.isdir(), "Got non directory input, breaking"

    paths = _collect_files_from_folder(p)
    items = [Item.from_path(str(f)) for f in paths]
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
                            flatten_result_folder=False):
    """

    :param task: the task object to process
    :type task: AlbumTask
    :param expected_artist: the artist name (optional)
    :param expected_album: the album name (optional)
    :param should_move:
    :param flatten_result_folder:
    :return:
    """
    logger.info("Started post processing for {}".format(task.id))
    logger.debug("Collecting media items from folders")

    aid_tagger = AcoustIDAlbumTagger()
    beets_tagger = BeetsTagger()
    renamer = Renamer()

    beets_tagger.process(task, expected_artist=expected_artist, expected_album=expected_album,
                         fallback_taggers=[aid_tagger])

    renamer.process(task, flatten_folder=flatten_result_folder)

    task.write_metadata_changes()
    task.write_to_disk(should_move=should_move)

    logger.info("Post processor compelted for {}".format(task.id))
