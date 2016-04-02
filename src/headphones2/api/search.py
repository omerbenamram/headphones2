from __future__ import unicode_literals, absolute_import, print_function, division
from pies.overrides import *

from headphones2.external.musicbrainz import find_artist_by_name
import logbook

if PY2:
    from headphones2.compat.http import HTTPStatus as HTTPStatus

if PY3:
    from http import HTTPStatus

import flask
from flask import abort, jsonify
from flask.blueprints import Blueprint

search_api = Blueprint('search', __name__, url_prefix='/api')
logger = logbook.Logger('api.search', level=logbook.DEBUG)
logger.handlers.append(logbook.StderrHandler())


@search_api.route('/search')
def search_musicbrainz_for_artist():
    args = flask.request.args
    search_type, q = args.get('type'), args.get('q')
    logger.debug('Search called with: {search_type}, {q}'.format(search_type=search_type, q=q))
    if not all([search_type, q]):
        abort(HTTPStatus.PRECONDITION_REQUIRED.value)  # Missing HTTP Parameters

    if search_type == 'artist':
        results = find_artist_by_name(q, limit=10)

        return jsonify({
            'data':
                [
                    {
                        'score': result['ext:score'],
                        'id': result['id'],
                        'uniqueName': result['name']
                    }
                    for result in results]
        })

    abort(HTTPStatus.PRECONDITION_FAILED.value)
