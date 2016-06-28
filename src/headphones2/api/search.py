from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import logbook
from musicbrainzngs import MusicBrainzError

from headphones2.cache import cache
from headphones2.external.musicbrainz import find_artist_by_name, find_releases
from headphones2.utils.general import make_cache_key

import flask
from flask import abort, jsonify
from flask.blueprints import Blueprint
from headphones2.compat import HTTPStatus

search_api = Blueprint('search', __name__, url_prefix='/api')
logger = logbook.Logger('api.search', level=logbook.DEBUG)
logger.handlers.append(logbook.StderrHandler())


@search_api.route('/search')
@cache.cached(timeout=6000, key_prefix=make_cache_key)
def search_musicbrainz():
    args = flask.request.args
    search_type, q = args.get('type'), args.get('q')
    logger.debug('Search called with: {search_type}, {q}'.format(search_type=search_type, q=q))
    if not all([search_type, q]):
        abort(HTTPStatus.BAD_REQUEST.value)  # Missing HTTP Parameters

    if search_type == 'artist':
        try:
            results = find_artist_by_name(q, limit=10)
        except MusicBrainzError:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR.value)

        return jsonify(dict(data=[
            {
                'score': result['ext:score'],
                'id': result['id'],
                'uniqueName': result['name']
            }
            for result in results], type='artist'))
    elif search_type == 'release':
        try:
            results = find_releases(q, limit=10)
        except MusicBrainzError:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR.value)

        return jsonify(dict(data=[
            {
                'score': result['ext:score'],
                'id': result['id'],
                'title': result['title'],
            }
            for result in results], type='release'))

    abort(HTTPStatus.BAD_REQUEST.value)
