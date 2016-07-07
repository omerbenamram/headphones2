from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook
import musicbrainzngs
import time
import sys

from redis.lock import Lock
from retry import retry
import redis

from beets.autotag.mb import album_info

RELEASE_INCLUDES = ['media', 'recordings', 'release-groups', 'labels', 'artist-credits']

MUSICBRAINZ_SLEEP_TIME = 8  # over time, this seems to be a nice sweetspot

musicbrainzngs.set_useragent("headphones2", "0.0", "https://github.com/omerbenamram/headphones2")
musicbrainzngs.set_hostname("musicbrainz.org:80")
musicbrainzngs.set_rate_limit()
logger = logbook.Logger(__name__)
logger.handlers.append(logbook.StreamHandler(sys.stdout))

# Lock for multi-process workers
local_redis = redis.Redis()


class MusicbrainzLock(Lock):
    def __enter__(self):
        super(MusicbrainzLock, self).__enter__()
        logger.debug('MusicbrainzLock acquired')

    def __exit__(self, exc_type, exc_val, exc_tb):
        # we ALWAYS Sleep after completion of job
        super(MusicbrainzLock, self).__exit__(exc_type, exc_val, exc_tb)
        logger.debug('Sleeping for {} seconds to avoid rate-limit'.format(MUSICBRAINZ_SLEEP_TIME))
        time.sleep(MUSICBRAINZ_SLEEP_TIME)
        logger.debug('Finished Sleep')
        logger.debug('MusicbrainzLock released')


musicbrainz_lock = MusicbrainzLock(local_redis, 'musicbrainz', sleep=MUSICBRAINZ_SLEEP_TIME, thread_local=False)


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def get_release_group_by_release_id(release_id):
    with musicbrainz_lock:
        results = musicbrainzngs.get_release_by_id(release_id, includes='release-groups')
        if results:
            return results['release']['release-group']['id']
        return None


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def get_artwork_for_album(rgid):
    """
    returns a dict with 'large' and 'small' using musicbrainz api
    """
    with musicbrainz_lock:
        logger.debug('fetching album art for album {id}'.format(id=rgid))
        results = {'small': 'http://coverartarchive.org/release-group/{rgid}/front-250.jpg'.format(rgid=rgid),
                   'large': 'http://coverartarchive.org/release-group/{rgid}/front-500.jpg'.format(rgid=rgid)}
        return results


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def get_release_groups_for_artist(artist_id, fetch_extras=False):
    with musicbrainz_lock:
        return musicbrainzngs.browse_release_groups(artist=artist_id, release_type=None if fetch_extras else 'album')[
            'release-group-list']


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def get_releases_for_release_group(release_group_id, includes=RELEASE_INCLUDES):
    with musicbrainz_lock:
        logger.debug('Fetching release for rgid {}'.format(release_group_id))
        search_results = musicbrainzngs.browse_releases(release_group=release_group_id,
                                                        release_type='album', includes=includes)['release-list']

        return [album_info(release) for release in search_results]


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def find_artist_by_name(name, limit=10, wanted_keys=('name', 'id', 'country', 'ext:score', 'type')):
    with musicbrainz_lock:
        params = {'artist': name.lower(), 'alias': name.lower()}
        search_results = musicbrainzngs.search_artists(limit=limit, **params)['artist-list']
        sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
        # return a list of dicts containing only the wanted values
        return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def find_releases(name, limit=10, artist_id=None,
                  wanted_keys=('name', 'id', 'title', 'country', 'release-group', 'ext:score', 'asin')):
    with musicbrainz_lock:
        strict = True if artist_id else False
        params = {'release': name, 'arid': artist_id}
        search_results = musicbrainzngs.search_releases(limit=limit, strict=strict, **params)['release-list']
        sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
        return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]


@retry(musicbrainzngs.MusicBrainzError, tries=3, delay=5, backoff=2, logger=logger)
def find_albums(name, limit=10, artist_id=None,
                wanted_keys=(
                        'name', 'id', 'title', 'country', 'release-group', 'ext:score', 'asin', 'artist-credit',
                        'type')):
    with musicbrainz_lock:
        strict = True if artist_id else False
        params = {'releasegroup': name, 'arid': artist_id}
        search_results = musicbrainzngs.search_release_groups(limit=limit, strict=strict, **params)[
            'release-group-list']
        sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
        return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]
