from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook

from beets.autotag import tag_album, Recommendation
from beets.library import Item

import six
from headphones2.utils.general import is_media_file

logger = logbook.Logger(__name__)


def identify_album_from_multiple_paths(paths_list_or_beets_items_list=None, expected_artist=None, expected_album=None,
                                       expected_release_id=None):
    items = paths_list_or_beets_items_list

    if isinstance(paths_list_or_beets_items_list[0], six.string_types):
        items = [Item.from_path(x) for x in paths_list_or_beets_items_list if is_media_file(x)]

    logger.debug("Called with {} items, expected id {}".format(len(items), expected_release_id))
    artist_name, album_name, album_recommendation_list, recommendation = \
        tag_album(items, search_artist=expected_artist, search_album=expected_album,
                  search_ids=[expected_release_id] if expected_release_id else [])

    if recommendation is Recommendation.none:
        return None, None

    distance, album_info, track_mapping, extra_items, extra_tracks = album_recommendation_list[0]
    logger.debug('Successfully matched album {} !'.format(album_info.album_id))

    logger.info("Successfully tagged album {album_id}, releasegroup {rgid}".format(album_id=album_info.album_id,
                                                                                   rgid=album_info.releasegroup_id))

    return album_info, track_mapping
