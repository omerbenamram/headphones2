from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook
import sys
from flask import Blueprint, request, abort, jsonify
from pies.overrides import *

from headphones2.configuration.scema import ConfigurationSchema
from headphones2.configuration.utils import dump_configuration, load_configuration_from_disk

if PY2:
    from headphones2.compat.http import HTTPStatus as HTTPStatus

if PY3:
    from http import HTTPStatus

logger = logbook.Logger(level=logbook.DEBUG)
logger.handlers.append(logbook.StreamHandler(sys.stdout))

configuration_api = Blueprint('configuration_api', __name__, url_prefix='/api')


@configuration_api.route('/configuration', methods=['GET'])
def get_configuration():
    current_configuration = load_configuration_from_disk()
    return jsonify({
        'data': ConfigurationSchema().dump(current_configuration)
    })


@configuration_api.route('/configuration', methods=['PUT', 'POST', 'PATCH'])
def update_configuration():
    request_data = request.get_json(force=True)
    new_configuration, errors = ConfigurationSchema().load(request_data)
    if errors:
        abort(HTTPStatus.BAD_REQUEST.value)

    dump_configuration(configuration=new_configuration)

    return ('', HTTPStatus.OK.value)
