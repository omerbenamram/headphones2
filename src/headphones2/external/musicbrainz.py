import musicbrainzngs

musicbrainzngs.set_useragent("test", "0.1", "https://github.com/test/pasten3")
musicbrainzngs.set_hostname("musicbrainz.org" + ":" + str(80))


def get_artwork_for_album(rgid):
    """
    returns a dict with 'large' and 'small' using musicbrainz api
    """
    try:
        cover_art = musicbrainzngs.get_release_group_image_list(rgid)
        return cover_art['images'][0]['thumbnails']
    except musicbrainzngs.ResponseError:
        return None


def get_release_groups_for_artist(artist_id, fetch_extras=False):
    return musicbrainzngs.browse_release_groups(artist=artist_id,
                                                release_type=None if fetch_extras else 'album')['release-group-list']


def get_releases_for_release_group(release_group_id, includes='recordings',
                                   wanted_keys=('barcode', 'title', 'country', 'medium-list', 'date', 'id', 'asin')):
    search_results = \
    musicbrainzngs.browse_releases(release_group=release_group_id, release_type='album', includes=[includes])[
        'release-list']
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in search_results]


def find_artist_by_name(name, limit=10, wanted_keys=('name', 'id', 'country', 'ext:score', 'type')):
    params = {'artist': name.lower(), 'alias': name.lower()}
    search_results = musicbrainzngs.search_artists(limit=limit, **params)['artist-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    # return a list of dicts containing only the wanted values
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]


def find_releases(name, limit=10, artist_id=None,
                  wanted_keys=('name', 'id', 'title', 'country', 'release-group', 'ext:score', 'asin')):
    strict = True if artist_id else False
    params = {'release': name, 'arid': artist_id}
    search_results = musicbrainzngs.search_releases(limit=limit, strict=strict, **params)['release-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]


def find_albums(name, limit=10, artist_id=None,
                wanted_keys=(
                        'name', 'id', 'title', 'country', 'release-group', 'ext:score', 'asin', 'artist-credit',
                        'type')):
    strict = True if artist_id else False
    params = {'releasegroup': name, 'arid': artist_id}
    search_results = musicbrainzngs.search_release_groups(limit=limit, strict=strict, **params)['release-group-list']
    sorted_by_score = sorted(search_results, cmp=lambda x, y: max(x, y), key=lambda d: int(d['ext:score']))
    return [{k: v for k, v in d.items() if k in wanted_keys} for d in sorted_by_score]