import musicbrainzngs
import logbook

logger = logbook.Logger(__name__)


def find_artist_by_name(name, limit=10, wanted_keys=('name', 'id', 'country', 'ext:score', 'type')):
    params = {'artist': name.lower(), 'alias': name.lower()}
    search_results = musicbrainzngs.search_artists(limit=limit, **params)['artist-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    # return a list of dicts containing only the wanted values
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]

