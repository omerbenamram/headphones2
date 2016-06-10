from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import Counter
from string import Template
import os

import py
import logbook

import six
from beetsplug.ftintitle import split_on_feat
from headphones2.postprocess.component_base import PostProcessor

logger = logbook.Logger(__name__)
Path = py.path.local


class Renamer(PostProcessor):
    def __init__(self):
        super(Renamer, self).__init__()

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
        return {k: six.u(str(v)) for k, v in six.iteritems(components)}

    def process(self, task, name_template="$SortArtist/$Album [$Year]/ $Track_num - $Track_name",
                destination_folder=str(Path(os.path.expanduser("~")).join("Music")), flatten_folder=False):
        """
        renamer main logic function

        :param task: task to process
        :type task: AlbumTask
        :param name_template: a formatted string containing any of: $Album,$Track_name,$Track_num",$Artist,$SortArtist,$
                                                                    $DiscNumber,$Year,$Genre
                                                                    / is used to specify wanted folder hierarchy

        :param destination_folder: base path for desitanation folder, defaults to $home/user/Music
        :param flatten_folder: True to coerce renamer to a single destination folder.
               uses most common sortartist to decide on folder
        :return: True if successful
        """

        components_dict = {item: self._components_from_item(item) for item in task}

        # Restrict output to one SortArtist, useful in many albums with lots of fts
        if flatten_folder:
            all_sort_artists = map(lambda x: x['SortArtist'], components_dict.values())
            most_common_sort_artist = Counter(all_sort_artists).most_common()[0][0]
            # override all other SortArtists
            for k in components_dict.values():
                k[six.u('SortArtist')] = most_common_sort_artist

        for item in task:
            original_path = Path(item.path)

            template = Template(name_template)
            new_name = template.substitute(components_dict[item])

            new_name += original_path.ext
            destination_path = Path(destination_folder).join(new_name)

            logger.info("{orig} --> {new}".format(orig=original_path.basename, new=new_name))
            task.set_path_for_item(item, str(destination_path))

        return True
