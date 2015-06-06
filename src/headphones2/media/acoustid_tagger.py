# A modified version of beets AcoustID plugin

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import acoustid
import logbook
import contextlib

from collections import defaultdict
from beets import util
from headphones2.media.tagger import Tagger

API_KEY = '1vOwZtEn'
SCORE_THRESH = 0.5
TRACK_ID_WEIGHT = 10.0
COMMON_REL_THRESH = 0.6  # How many tracks must have an album in common?
MAX_RECORDINGS = 5
MAX_RELEASES = 5

logger = logbook.Logger(__name__)


class Task(object):
    def __init__(self, items, is_album=True):
        self.items = items
        self.is_album = is_album
        self.item = items[0]


class AcoustIDAlbumTagger(Tagger):
    def __init__(self, task):
        super(AcoustIDAlbumTagger, self).__init__(task)
        self._matches = {}
        # Stores the fingerprint and Acoustid ID for each track. This is stored
        # as metadata for each track for later use but is not relevant for
        # autotagging.
        self._fingerprints = {}
        self._acoustids = {}
        self._releases_results = []
        self._finished_running = False

    @property
    def results(self):
        if not self._releases_results:
            self.tag()
            self._releases_results = [r for r in self._match_releases()]

        return self._releases_results

    def _match_releases(self):
        """Given an iterable of Items, determines (according to Acoustid)
        which releases the items have in common. Generates release IDs.
        """
        # Count the number of "hits" for each release.
        relcounts = defaultdict(int)
        for item in self._task.items:
            if item.path not in self._matches:
                continue

            _, release_ids = self._matches[item.path]
            for release_id in release_ids:
                relcounts[release_id] += 1

        for release_id, count in relcounts.iteritems():
            if float(count) / len(self._task.items) > COMMON_REL_THRESH:
                yield release_id

    def _acoustid_match(self, path):
        """Gets metadata for a file from Acoustid and populates the
        _matches, _fingerprints, and _acoustids dictionaries accordingly.
        """
        try:
            duration, fp = acoustid.fingerprint_file(util.syspath(path))
        except acoustid.FingerprintGenerationError as exc:
            logger.error(u'fingerprinting of {0} failed: {1}',
                         util.displayable_path(repr(path)), exc)
            return None
        self._fingerprints[path] = fp
        try:
            res = acoustid.lookup(API_KEY, fp, duration,
                                  meta='recordings releases')
        except acoustid.AcoustidError as exc:
            logger.debug(u'fingerprint matching {0} failed: {1}',
                         util.displayable_path(repr(path)), exc)
            return None
        logger.debug(u'chroma: fingerprinted {0}',
                     util.displayable_path(repr(path)))

        # Ensure the response is usable and parse it.
        if res['status'] != 'ok' or not res.get('results'):
            logger.debug(u'no match found')
            return None
        result = res['results'][0]  # Best match.
        if result['score'] < SCORE_THRESH:
            logger.debug(u'no results above threshold')
            return None
        self._acoustids[path] = result['id']

        # Get recording and releases from the result.
        if not result.get('recordings'):
            logger.debug(u'no recordings found')
            return None
        recording_ids = []
        release_ids = []
        for recording in result['recordings']:
            recording_ids.append(recording['id'])
            if 'releases' in recording:
                release_ids += [rel['id'] for rel in recording['releases']]

        logger.debug(u'matched recordings {0} on releases {1}',
                     recording_ids, release_ids)
        self._matches[path] = recording_ids, release_ids

    @contextlib.contextmanager
    def tag(self):
        """Fingerprint each item in the task"""
        items = self._task.items if self._task.is_album else [self._task.item]
        for item in items:
            self._acoustid_match(item.path)
        self._finished_running = True

    def apply_metadata(self):
        """Apply Acoustid metadata (fingerprint and ID) to the task's items.
        """
        for item in self._task.imported_items():
            if item.path in self._fingerprints:
                item.acoustid_fingerprint = self._fingerprints[item.path]
            if item.path in self._acoustids:
                item.acoustid_id = self._acoustids[item.path]

    def submit_items(self, userkey, items, chunksize=64):
        """Submit fingerprints for the items to the Acoustid server.
        """
        data = []  # The running list of dictionaries to submit.

        def submit_chunk():
            """Submit the current accumulated fingerprint data."""
            logger.info(u'submitting {0} fingerprints', len(data))
            try:
                acoustid.submit(API_KEY, userkey, data)
            except acoustid.AcoustidError as exc:
                logger.warn(u'acoustid submission error: {0}', exc)
            del data[:]

        for item in items:
            fp = self._fingerprint_item(item)

            # Construct a submission dictionary for this item.
            item_data = {
                'duration': int(item.length),
                'fingerprint': fp,
            }
            if item.mb_trackid:
                item_data['mbid'] = item.mb_trackid
                logger.debug(u'submitting MBID')
            else:
                item_data.update({
                    'track': item.title,
                    'artist': item.artist,
                    'album': item.album,
                    'albumartist': item.albumartist,
                    'year': item.year,
                    'trackno': item.track,
                    'discno': item.disc,
                })
                logger.debug(u'submitting textual metadata')
            data.append(item_data)

            # If we have enough data, submit a chunk.
            if len(data) >= chunksize:
                submit_chunk()

        # Submit remaining data in a final chunk.
        if data:
            submit_chunk()

    @staticmethod
    def _fingerprint_item(item, write=False):
        """Get the fingerprint for an Item. If the item already has a
        fingerprint, it is not regenerated
        If `write` is set, then the new fingerprints are also written to files' metadata.
        """
        # Get a fingerprint and length for this track.
        if not item.length:
            logger.info(u'{0}: no duration available',
                        util.displayable_path(item.path))
        elif item.acoustid_fingerprint:
            if write:
                logger.info(u'{0}: fingerprint exists, skipping',
                            util.displayable_path(item.path))
            else:
                logger.info(u'{0}: using existing fingerprint',
                            util.displayable_path(item.path))
                return item.acoustid_fingerprint
        else:
            logger.info(u'{0}: fingerprinting',
                        util.displayable_path(item.path))
            try:
                _, fp = acoustid.fingerprint_file(item.path)
                item.acoustid_fingerprint = fp
            except acoustid.FingerprintGenerationError as exc:
                logger.info(u'fingerprint generation failed: {0}', exc)

    @staticmethod
    def prefix(it, count):
        """Truncate an iterable to at most `count` items.
        """
        for i, v in enumerate(it):
            if i >= count:
                break
            yield v
