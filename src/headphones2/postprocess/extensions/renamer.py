# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import py
import os
import shutil

import logbook

from beetsplug.ftintitle import split_on_feat

from headphones2.postprocess.component_base import PostProcessorComponentBase

logger = logbook.Logger(__name__)
Path = py.path.local

class Renamer(PostProcessorComponentBase):
    modifies_file = True
    group = 'extension'

    def __init__(self):
        super(Renamer, self).__init__()

    @staticmethod
    def _components_from_item(item):
        """
        :param item:
        :type item: beets.library.Item
        :return: dictionary of track components
        :rtype dict
        """
        components = {
            "$Album": item.album,
            "$Track_name": item.title,
            "$Track_num": item.track,
            "$Artist": item.artist,
            "$SortArtist": split_on_feat(item.artist)[0],
            "$DiscNumber": item.disc,
            "$Year": item.year,
            "$Genre": item.genre
        }

        return {unicode(k): unicode(v) for k, v in components.iteritems()}

    @staticmethod
    def process(item_list, name_string="$SortArtist/$Album [$Year]/ $Track_num - $Track_name",
                destination_folder=unicode(Path(os.path.expanduser("~")).join("Music")),
                release_id=None, should_move=False):

        # decide if we want to keep original files
        operation = shutil.move if should_move else shutil.copy

        for item in item_list:
            components = Renamer._components_from_item(item)

            original_path = Path(item.path)
            new_name = name_string

            for param, value in components.iteritems():
                new_name = new_name.replace(param, value)

            new_name += original_path.ext
            destination_path = Path(destination_folder).join(new_name)

            logger.info("Renaming {orig} --> {new}".format(orig=original_path.basename, new=new_name))

            if not destination_path.join(os.path.pardir).exists():
                os.makedirs(unicode(destination_path.dirpath()))

            logger.info("{action} {orig} --> {new}".format(action=("Moving" if should_move else "Copying"),
                                                           orig=original_path, new=destination_path))
            operation(item.path, unicode(destination_path))

        return True
