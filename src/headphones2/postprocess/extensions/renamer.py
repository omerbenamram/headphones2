from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import Counter
from pies.overrides import *

from string import Template
import py
import os
import logbook

from beetsplug.ftintitle import split_on_feat

from headphones2.postprocess.component_base import PostProcessor

logger = logbook.Logger(__name__)
Path = py.path.local

class Renamer(PostProcessor):

    def __init__(self):
        super(Renamer, self).__init__()
        self.destination_paths = {}

    def _components_from_item(self, item):
        """
        :param item:
        :type item: beets.library.Item
        :return: dictionary of track components
        :rtype dict
        """
        components = {
            "Album": item.album,
            "Track_name": item.title,
            "Track_num": item.track,
            "Artist": item.artist,
            "SortArtist": split_on_feat(item.artist)[0],  # Gorillaz ft the doors --> ('Gorillaz', 'The Doors')
            "DiscNumber": item.disc,
            "Year": item.year,
            "Genre": item.genre
        }
        return {k: unicode(v) for k, v in components.iteritems()}

    def process(self, item_list, name_template="$SortArtist/$Album [$Year]/ $Track_num - $Track_name",
                destination_folder=str(Path(os.path.expanduser("~")).join("Music")), flatten_folder=False):
        """
        renamer main logic function

        :param item_list: list of items to process
        :type item_list: list[beets.library.Item]
        :param name_template: a formatted string containing any of: $Album,$Track_name,$Track_num",$Artist,$SortArtist,$
                                                                    $DiscNumber,$Year,$Genre
                                                                    / is used to specify wanted folder hierarchy

        :param destination_folder: base path for desitanation folder, defaults to $home/user/Music
        :param flatten_folder: True to coerce renamer to a single destination folder.
               uses most common sortartist to decide on folder
        :return: True if successful
        """

        components_dict = {item: self._components_from_item(item) for item in item_list}

        # Restrict output to one SortArtist, useful in many albums with lots of fts
        if flatten_folder:
            all_sort_artists = map(lambda x: x['SortArtist'], components_dict.values())
            most_common_sort_artist = Counter(all_sort_artists).most_common()[0][0]
            # override all other SortArtists
            for k in components_dict.values():
                k['SortArtist'] = most_common_sort_artist

        for item in item_list:
            original_path = Path(item.path)

            template = Template(name_template)
            new_name = template.substitute(components_dict[item])

            new_name += original_path.ext
            destination_path = Path(destination_folder).join(new_name)

            logger.info("{orig} --> {new}".format(orig=original_path.basename, new=new_name))
            self.destination_paths[str(original_path)] = str(destination_path)

        return True

    def write(self, item_list, should_move=False, **kwargs):
        """
        :param item_list:
        :type item_list: list[beets.library.Item]
        :param should_move:
        :return:
        """
        # beets use "should copy"..
        copy = not should_move

        for item in item_list:
            dest_path = self.destination_paths[item.path]
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))

            item.move_file(dest_path, copy=copy)
            logger.info("{action} {orig} --> {new}".format(action=("Moving" if should_move else "Copying"),
                                                           orig=item.path, new=dest_path))