from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import uuid

import logbook
from builtins import str
from beets.autotag import apply_metadata

logger = logbook.Logger(__name__)


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

    @property
    def is_completed(self):
        return all(map(lambda x: x is not None, [self._album_info_object, self._track_mapping_object]))

    def __len__(self):
        return len(self._item_list)

    def __iter__(self):
        for item in self._item_list:
            yield item

    def __repr__(self):
        return "<Task {id} - Artist: {artist}, Album: {album}, Items: {items}>".format(
            id=self.id,
            artist=(self._album_info_object.artist if self._album_info_object else '?'),
            album=(self._album_info_object.album if self._album_info_object else '?'),
            items=len(self))

    def set_path_for_item(self, item, new_path):
        assert isinstance(new_path, str), "Path must be a string!"
        self._path_mapping[item.path] = new_path

    def write_metadata_changes(self):
        assert self.is_completed, "Processing is not finished for task {}".format(self.id)
        apply_metadata(self._album_info_object, self._track_mapping_object)

        for item in self:
            item.write()

    def write_to_disk(self, should_move):
        assert len(self._path_mapping) == len(self)
        # beets use "should copy"..
        copy = not should_move

        for item in self:
            destination_path = self._path_mapping[item.path]
            if not os.path.exists(os.path.dirname(destination_path)):
                os.makedirs(os.path.dirname(destination_path))

            item.move_file(destination_path, copy=copy)
            logger.info("{action} {orig} --> {new}".format(action=("Moving" if should_move else "Copying"),
                                                           orig=item.path, new=destination_path))
