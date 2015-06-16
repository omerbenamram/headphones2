from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import namedtuple
from collections import Counter
from itertools import chain

import acoustid
import logbook
import musicbrainzngs
import py

from headphones2.postprocess.component_base import PostProcessorComponentBase

Path = py.path.local

logger = logbook.Logger(__name__)

API_KEY = '1vOwZtEn'
SCORE_THRESH = 0.5
TRACK_ID_WEIGHT = 10.0
COMMON_REL_THRESH = 0.6  # How many tracks must have an album in common?
MAX_RECORDINGS = 5
MAX_RELEASES = 5


class AcoustIDAlbumTagger(PostProcessorComponentBase):

    def __init__(self):
        super(AcoustIDAlbumTagger, self).__init__()

    Result = namedtuple('Result', ['fingerprint', 'acoustid', 'recording_id', 'release_id'])

    @staticmethod
    def _match_releases(result_list):
        """
        determines which releases the items have in common.
        also uses number of tracks to make sure its the same release
        """
        result_ids = chain.from_iterable([result.release_id for result in result_list if result])
        top_matches = Counter(result_ids).most_common(MAX_RELEASES)
        num_of_tracks = len(result_list)

        for release_id, _ in top_matches:
            r = musicbrainzngs.get_release_by_id(release_id, includes='recordings')
            mediums = r['release']['medium-list']
            tracks = sum([mediums[i]['track-count'] for i, j in enumerate(mediums)])
            if tracks == num_of_tracks:
                return release_id

        return None

    @staticmethod
    def _acoustid_tag_file(filepath):
        """
        Gets metadata for a file from Acoustid.
        returns a Result object with Fingerprint, acoustid, recording_ids and release_ids
        """
        path = Path(filepath)
        try:
            duration, fingerprint = acoustid.fingerprint_file(str(path))
        except acoustid.FingerprintGenerationError as exc:
            logger.error(u'fingerprinting of {0} failed: {1}', filepath, exc)
            return None

        try:
            res = acoustid.lookup(API_KEY, fingerprint, duration, meta='recordings releases')
        except acoustid.AcoustidError as exc:
            logger.debug(u'fingerprint matching {0} failed: {1}', filepath, exc)
            return None

        logger.debug(u'fingerprinted {0}', filepath)

        # Ensure the response is usable and parse it.
        if res['status'] != 'ok' or not res.get('results'):
            logger.debug(u'no match found')
            return None

        acoustid_result = res['results'][0]  # Best match.
        if acoustid_result['score'] < SCORE_THRESH:
            logger.debug(u'no results above threshold')
            return None

        # Get recording and releases from the result.
        if not acoustid_result.get('recordings'):
            logger.debug(u'no recordings found')
            return None

        recording_ids = []
        release_ids = []

        for recording in acoustid_result['recordings']:
            recording_ids.append(recording['id'])
            if 'releases' in recording:
                release_ids += [rel['id'] for rel in recording['releases']]

        logger.debug(u'matched recordings {0} on releases {1}', recording_ids, release_ids)

        return AcoustIDAlbumTagger.Result(fingerprint, acoustid_result['id'], recording_ids, release_ids)

    @staticmethod
    def process(item_list):
        results = {item: AcoustIDAlbumTagger._acoustid_tag_file(item.path) for item in item_list}

        for item, result in results.iteritems():
            if not result:
                continue
            item.acoustid_fingerprint = result.fingerprint
            item.acoustid_id = result.acoustid
            logger.debug('Writing metadata modifications to file {}'.format(item.path))
            item.write()

        identified_release = AcoustIDAlbumTagger._match_releases(results.values())
        if identified_release is not None:
            return True, identified_release

        return False
