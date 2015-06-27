from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook

from beets.autotag import tag_album, Recommendation
from headphones2.postprocess.component_base import PostProcessor, PostProcessorException

logger = logbook.Logger(__name__)


class BeetsTagger(PostProcessor):
    def __init__(self):
        super(BeetsTagger, self).__init__()

    def process(self, task, expected_artist=None, expected_album=None, expected_release_id=None,
                fallback_taggers=()):
        """
        :param task: the task object to tag
        :param expected_artist: the artist name (not id) to help matching
        :type expected_artist: str
        :param expected_album: the album name (not id) to help matching
        :type expected_album: str
        :param expected_release_id: expected release id to help tagger (this might cause wrong results, use with care!)
        :param fallback_taggers: a list of fallback taggers to help tag if no recommendations are extracted from metadata
        :type fallback_taggers: list[PostProcessor]
        :rtype BeetsTaggerResult
        :return: a result object containing album_id, album_info_object, track_mapping_object,
                                            extra_items and extra_tracks
        """
        artist_name, album_name, album_recommendation_list, recommendation = \
            tag_album(task.items, search_artist=expected_artist, search_album=expected_album,
                      search_id=expected_release_id)

        if recommendation is Recommendation.none:
            logger.warning('{} Failed to match album'.format(__name__))

            if not fallback_taggers:
                raise BeetsTaggerException("Exhausted all tagging options, failing")

            for tagger in fallback_taggers:
                logger.debug("Calling {}".format(tagger.__class__.__name__))
                fallback_recommendation = tagger.process(task)
                if not fallback_recommendation:
                    continue

                artist_name, album_name, album_recommendation_list, recommendation = \
                    tag_album(task.items, search_artist=expected_artist, search_album=expected_album,
                              search_id=fallback_recommendation)

        if recommendation is Recommendation.none:
            raise BeetsTaggerException("Exhausted all tagging options, failing")

        distance, album_info, track_mapping, extra_items, extra_tracks = album_recommendation_list[0]
        logger.debug('Successfully matched album {} !'.format(album_info.album_id))

        logger.info("Successfully tagged album {album_id}, releasegroup {rgid}".format(album_id=album_info.album_id,
                                                                                       rgid=album_info.releasegroup_id))

        task._album_info_object = album_info
        task._track_mapping_object = track_mapping

        return True


class BeetsTaggerException(PostProcessorException):
    pass
