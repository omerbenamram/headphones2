from __future__ import (absolute_import, division, print_function, unicode_literals)

import flask
import logbook
import requests

from flask.blueprints import Blueprint
from flask import abort

from headphones2.external.lastfm import lastfm_api_wrapper
from headphones2.tasks import get_artwork_for_album_task

logger = logbook.Logger()

artwork_api = Blueprint('artwork_api', __name__, url_prefix='/api')


@artwork_api.route('/artwork', methods=['GET'])
def get_artwork():
    args = flask.request.args
    image_type = args.get('type')
    if not image_type:
        abort(422)

    mbid, size, should_fetch_image = args.get('id'), args.get('size'), args.get('fetch_image')
    if image_type == 'artist':
        return _get_artist_artwork(mbid=mbid, size=size, fetch_image=should_fetch_image)
    elif image_type == 'album':
        return _get_album_cover_art(rgid=mbid, size=size, fetch_image=should_fetch_image)
    else:
        abort(406)  # Bad Params supplied


def _get_album_cover_art(rgid, size='small', fetch_image=False):
    """
    :param rgid: musicbrainz releasegroup_id
    :param size: large (500px) or small (250px)
    :return: binary jpeg
    """
    urls = get_artwork_for_album_task(rgid).get(True)
    if not urls:
        abort(404)

    chosen = urls.get(size)
    if not fetch_image:
        return chosen

    img = requests.get(chosen)
    if not img.ok:
        abort(404)

    resp = flask.make_response(img.content)
    resp.content_type = "image/jpeg"
    return resp


def _get_artist_artwork(mbid, size='small', fetch_image=False):
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

    if not fetch_image:
        return size_dict[size]

    img = requests.get(size_dict[size])

    if not img.ok:
        abort(404)

    resp = flask.make_response(img.content)
    resp.content_type = "image/jpeg"
    return resp
