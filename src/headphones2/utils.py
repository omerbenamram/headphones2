import musicbrainzngs
import logbook

logger = logbook.Logger(__name__)


def find_artist_by_name(name, limit=10, wanted_keys=('name', 'id', 'country', 'ext:score', 'type')):
    params = {'artist': name.lower(), 'alias': name.lower()}
    search_results = musicbrainzngs.search_artists(limit=limit, **params)['artist-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    # return a list of dicts containing only the wanted values
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]

# TODO: search by releasegrouop ID
def find_releases(name, limit=10, artist_id=None,
                  wanted_keys=('name', 'id', 'title', 'country', 'release-group', 'ext:score', 'asin')):
    params = {'release': name, 'arid': artist_id}
    search_results = musicbrainzngs.search_releases(limit=limit, **params)['release-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]

# TODO: return better dict
def find_albums(name, limit=10, artist_id=None,
                wanted_keys=('name', 'id', 'title', 'country', 'release-group', 'ext:score', 'asin', 'artist-credit')):
    params = {'releasegroup': name, 'arid': artist_id}
    search_results = musicbrainzngs.search_release_groups(limit=limit, strict=True, **params)['release-group-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]
