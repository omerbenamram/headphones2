from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

import logbook
from headphones2.tasks import add_artist_task, add_album_from_folder_to_db, fetch_albums_from_root_directory

logger = logbook.Logger(__name__)


# this currently wont handle changes. it should
def import_library(root_path):
    logbook.info('Starting to import library at path {}'.format(root_path))
    assert os.path.isdir(root_path), '{} must be a directory!'.format(root_path)

    results = fetch_albums_from_root_directory(root_path)

    artists_ids_to_add_to_db = {album_items_info_tuple.album_tracks_info_tuple.album_info.artist_id for
                                album_items_info_tuple in results}

    for artist_id in artists_ids_to_add_to_db:
        add_artist_task(artist_id=artist_id)

        for folder, album_items_info_tuple in results:
            logger.debug('Working on folder {}'.format(folder))
            add_album_from_folder_to_db(album_items_info_tuple, artist_id)


