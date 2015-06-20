from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook

from beets.autotag import tag_album, Recommendation, apply_metadata
from headphones2.postprocess.component_base import PostProcessor, PostProcessorException

logger = logbook.Logger(__name__)


class SimpleBeetsTagger(PostProcessor):

    def __init__(self):
        super(SimpleBeetsTagger, self).__init__()

    @staticmethod
    def process(list_of_items, expected_artist=None, expected_album=None, expected_release_id=None):
        artist_name, album_name, album_recommendation_list, recommendation = \
            tag_album(list_of_items, search_artist=expected_artist, search_album=expected_album, search_id=expected_release_id)

        if recommendation is Recommendation.none:
            logger.debug('{} Failed to match album'.format(__name__))
            raise PostProcessorException('{} Failed to match album'.format(__name__))

        distance, album_info, track_mapping, extra_items, extra_tracks = album_recommendation_list[0]
        apply_metadata(album_info, track_mapping)

        logger.info("Successfully tagged album {album_id}, releasegroup {rgid}".format(album_id=album_info.album_id,
                                                                                       rgid=album_info.releasegroup_id))
        return True, album_info.album_id
