from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

import logbook
from beets.importer import albums_in_dir
from headphones2.taggers.pipeline import match_album_from_list_of_paths
from headphones2.tasks import add_artist_task
from headphones2.utils.structs import FolderResult

logger = logbook.Logger(__name__)


# TODO: implement
def add_track_mapping_to_db(items_to_trackinfo_mapping):
    pass


# this currently wont handle changes. it should
def import_library(root_path):
    logbook.info('Starting to import library at path {}'.format(root_path))
    assert os.path.isdir(root_path), '{} must be a directory!'.format(root_path)

    results = [FolderResult(folder, match_album_from_list_of_paths(list_of_files)) for folder, list_of_files in
               list(albums_in_dir(root_path))]

    artists_to_add_to_db = {album_items_info_tuple.album_tracks_info_tuple.album_info.artist_id for
                            album_items_info_tuple in results}

    for artist_id in artists_to_add_to_db:
        add_artist_task(artist_id=artist_id)

        # for folder, album_items_info_tuple in results:
        #     logger.debug('Working on folder {}'.format(folder))
        #     for album_info, items_to_trackinfo_mapping in album_items_info_tuple:
        #         add_track_mapping_to_db(items_to_trackinfo_mapping)
