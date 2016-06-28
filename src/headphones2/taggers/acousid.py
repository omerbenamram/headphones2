from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import namedtuple

import acoustid
import logbook
import py
import six

from headphones2.taggers.common import _select_best_release_from_many

Path = py.path.local

logger = logbook.Logger(__name__)

SCORE_THRESH = 0.5
COMMON_REL_THRESH = 0.6  # How many tracks must have an album in common?
MAX_RELEASES = 5
API_KEY = '1vOwZtEn'

AcoustIDTaggerResult = namedtuple('Result', ['fingerprint', 'acoustid', 'recording_id', 'release_id'])


def _acoustid_tag_file(filepath):
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
        res = acoustid.lookup(API_KEY, fingerprint, duration, meta='recordings releases')
    except acoustid.AcoustidError as exc:
        logger.debug('fingerprint matching {0} failed: {1}', filepath, exc)
        return None

    logger.debug('fingerprinted {0}', filepath)

    # Ensure the response is usable and parse it.
    if res['status'] != 'ok' or not res.get('results'):
        logger.debug('no match found')
        return None

    acoustid_result = res['results'][0]  # Best match.
    if acoustid_result['score'] < SCORE_THRESH:
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


def identify_album_from_multiple_paths(list_of_paths, write_changes_to_items=False):
    """
    matches a release using acoustid
    :param item_list:
    :param kwargs:
    :return: release_id or None
    """
    results = {path: _acoustid_tag_file(path) for path in list_of_paths}

    if write_changes_to_items:
        for item, result in six.iteritems(results):
            if not result:
                continue
            item.acoustid_fingerprint = result.fingerprint
            item.acoustid_id = result.acoustid

    identified_release = _select_best_release_from_many(results.values())
    if identified_release is not None:
        return identified_release

    return None
