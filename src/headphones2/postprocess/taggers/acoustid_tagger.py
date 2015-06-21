from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import namedtuple
from collections import Counter
from itertools import chain

import acoustid
import logbook
import musicbrainzngs
import py

from headphones2.postprocess.component_base import PostProcessor

Path = py.path.local

logger = logbook.Logger(__name__)

AcoustIDTaggerResult = namedtuple('Result', ['fingerprint', 'acoustid', 'recording_id', 'release_id'])


class AcoustIDAlbumTagger(PostProcessor):

    SCORE_THRESH = 0.5
    COMMON_REL_THRESH = 0.6  # How many tracks must have an album in common?
    MAX_RELEASES = 5

    def __init__(self, api_key='1vOwZtEn'):
        super(AcoustIDAlbumTagger, self).__init__()
        self.api_key = api_key

    def _match_releases(self, result_list):
        """
        determines which releases the items have in common.
        also uses number of tracks to make sure its the same release
        """
        result_ids = chain.from_iterable([result.release_id for result in result_list if result])
        top_matches = Counter(result_ids).most_common(self.MAX_RELEASES)
        actual_number_of_tracks = len(result_list)

        for release_id, _ in top_matches:
            r = musicbrainzngs.get_release_by_id(release_id, includes='recordings')
            mediums = r['release']['medium-list']
            tracks = sum([mediums[i]['track-count'] for i, j in enumerate(mediums)])
            if tracks == actual_number_of_tracks:
                return release_id

        return None

    def _acoustid_tag_file(self, filepath):
        """
        Gets metadata for a file from Acoustid.
        returns a Result object with Fingerprint, acoustid, recording_ids and release_ids

        Suppresses all exceptions - will return None if failed
        """
        path = Path(filepath)
        try:
            duration, fingerprint = acoustid.fingerprint_file(str(path))
        except acoustid.FingerprintGenerationError as exc:
            logger.error('fingerprinting of {0} failed: {1}', filepath, exc)
            return None

        try:
            res = acoustid.lookup(self.api_key, fingerprint, duration, meta='recordings releases')
        except acoustid.AcoustidError as exc:
            logger.debug('fingerprint matching {0} failed: {1}', filepath, exc)
            return None

        logger.debug('fingerprinted {0}', filepath)

        # Ensure the response is usable and parse it.
        if res['status'] != 'ok' or not res.get('results'):
            logger.debug('no match found')
            return None

        acoustid_result = res['results'][0]  # Best match.
        if acoustid_result['score'] < self.SCORE_THRESH:
            logger.debug('no results above threshold')
            return None

        # Get recording and releases from the result.
        if not acoustid_result.get('recordings'):
            logger.debug('no recordings found')
            return None

        recording_ids = []
        release_ids = []

        for recording in acoustid_result['recordings']:
            recording_ids.append(recording['id'])
            if 'releases' in recording:
                release_ids += [rel['id'] for rel in recording['releases']]

        logger.debug('matched recordings {0} on releases {1}', recording_ids, release_ids)

        return AcoustIDTaggerResult(fingerprint, acoustid_result['id'], recording_ids, release_ids)

    def process(self, item_list, **kwargs):
        results = {item: self._acoustid_tag_file(item.path) for item in item_list}

        for item, result in results.iteritems():
            if not result:
                continue
            item.acoustid_fingerprint = result.fingerprint
            item.acoustid_id = result.acoustid

        identified_release = self._match_releases(results.values())
        if identified_release is not None:
            return True, identified_release

        return False, None

    def write(self, item_list, **kwargs):
        for item in item_list:
            item.write()
            logger.debug('Writing AcoustID metadata to file {}'.format(item.path))

        return
