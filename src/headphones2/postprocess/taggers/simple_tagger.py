from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import namedtuple

import logbook

from beets.autotag import tag_album, Recommendation, apply_metadata
from headphones2.postprocess.component_base import PostProcessor, PostProcessorException

logger = logbook.Logger(__name__)

BeetsTaggerResult = namedtuple("Result", ["album_id", "album_info_object", "track_mapping_object", "extra_items", "extra_tracks"])

class BeetsTagger(PostProcessor):
    def __init__(self):
        super(BeetsTagger, self).__init__()

    def process(self, list_of_items, expected_artist=None, expected_album=None, expected_release_id=None,
                fallback_tagger=None):
        artist_name, album_name, album_recommendation_list, recommendation = \
            tag_album(list_of_items, search_artist=expected_artist, search_album=expected_album,
                      search_id=expected_release_id)

        if recommendation is Recommendation.none:
            logger.debug('{} Failed to match album'.format(__name__))
            raise BeetsTaggerException('{} Failed to match album'.format(__name__))

        distance, album_info, track_mapping, extra_items, extra_tracks = album_recommendation_list[0]
        logger.debug('Successfully matched album {} !'.format(album_info.album_id))

        logger.info("Successfully tagged album {album_id}, releasegroup {rgid}".format(album_id=album_info.album_id,
                                                                                       rgid=album_info.releasegroup_id))

        return BeetsTaggerResult(album_info.album_id, album_info, track_mapping, extra_items, extra_tracks)

    def write(self, item_list, album_info=None, track_mapping=None, **kwargs):
        apply_metadata(album_info, track_mapping)
        return


class BeetsTaggerException(PostProcessorException):
    pass
