import os
import shutil

import logbook

from pathlib import Path

from headphones2.postprocess.component_base import PostProcessorComponentBase

logger = logbook.Logger(__name__)


class Renamer(PostProcessorComponentBase):
    kind = 'extension'

    def __init__(self):
        super(PostProcessorComponentBase, self).__init__()

    @staticmethod
    def _components_from_item(item):
        """
        :param item:
        :type item: beets.library.Item
        :return: dictionary of track components
        :rtype dict
        """
        return {
            "$Album": item.album,
            "$Track_name": item.title,
            "$Track_num": item.track,
            "$Artist": item.artist,
            "$SortArtist": "",  # TODO: decide if implement
            "$DiscNumber": item.disc,
            "$Year": item.year,
            "$Genre": item.genre
        }

    @staticmethod
    def process(item_list, name_string="$Artist/$Album [$Year]/ $Track_num - $Track_name",
                destination_folder=str(Path(os.path.expanduser("~")).joinpath("Music")),
                release_id=None, should_move=False):

        # decide if we want to keep original files
        operation = shutil.move if should_move else shutil.copy

        for item in item_list:
            components = Renamer._components_from_item(item)

            original_path = Path(item.path)
            new_name = name_string

            for param, value in components.iteritems():
                new_name = new_name.replace(param, str(value))

            new_name += original_path.suffix
            new_path = Path(new_name)
            logger.info("Renaming {orig} --> {new}".format(orig=original_path.name, new=new_path.name))

            destination_path = Path(destination_folder).joinpath(new_path)
            if not destination_path.exists():
                os.makedirs(str(destination_path))

            logger.info("Moving {orig} --> {new}".format(orig=original_path, new=destination_path))
            operation(item.path, str(destination_path))

        return True
