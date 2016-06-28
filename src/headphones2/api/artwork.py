from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import flask
import logbook
from flask import abort, jsonify
from flask.blueprints import Blueprint

from headphones2.cache import cache
from headphones2.external.lastfm import lastfm_api_wrapper
from headphones2.tasks import get_artwork_for_album_task
from headphones2.utils.general import make_cache_key

logger = logbook.Logger()

artwork_api = Blueprint('artwork_api', __name__, url_prefix='/api')


@artwork_api.route('/artwork', methods=['GET'])
@cache.cached(timeout=6000, key_prefix=make_cache_key)
def get_artwork():
    args = flask.request.args
    image_type = args.get('type')
    if not image_type:
        abort(422)

    mbid, size = args.get('id'), args.get('size')
    if image_type == 'artist':
        url = _get_artist_artwork(mbid=mbid, size=size)
    elif image_type == 'album':
        url = _get_album_cover_art(rgid=mbid, size=size)
    else:
        abort(406)  # Bad Params supplied

    return jsonify({
        'data': url
    })


def _get_album_cover_art(rgid, size='small'):
    """
    :param rgid: musicbrainz releasegroup_id
    :param size: large (500px) or small (250px)
    :return: binary jpeg
    """
    urls = get_artwork_for_album_task(rgid).get(True)
    if not urls:
        abort(404)

    return urls.get(size)


def _get_artist_artwork(mbid, size='small'):
    """
    :param mbid: musicbrainz artist_id
    :param size: large (500px) or small (250px)
    :return: binary jpeg
    """
    artist_info = lastfm_api_wrapper("artist.getinfo", mbid=mbid)
    if not artist_info:
        abort(404)

    artist_artwork = artist_info['artist']['image']
    # convert response list of dicts to something more usable
    size_dict = {d['size']: d['#text'] for d in artist_artwork}
    chosen = size_dict[size]
    if not chosen:
        logger.warning(('No image found for ({id}, {size}'.format(id=mbid, size=size)))
        abort(404)

    return size_dict[size]
