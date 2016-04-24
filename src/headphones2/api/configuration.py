from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import simplejson as json
import sys

# noinspection PyUnresolvedReferences
from flask import Blueprint, request, abort
from pies.overrides import *
from headphones2.config import CONFIGURATION_PATH
from marshmallow import Schema, fields, validates
import logbook

from headphones2.utils.filesystem import is_pathname_valid

logger = logbook.Logger(level=logbook.DEBUG)
logger.handlers.append(logbook.StreamHandler(sys.stdout))

configuration_api = Blueprint('artist_api', __name__, url_prefix='/api')


class ConfigurationSchema(Schema):
    libraryPath = fields.Str()
    debug = fields.Boolean()

    @validates('libraryPath')
    def validate_path(self, value):
        return is_pathname_valid(value)


@configuration_api.route('/configuration', methods=['GET'])
def get_headphones_configuration():
    try:
        with open(CONFIGURATION_PATH, str('rb')) as fp:
            current_configuration = json.load(fp)
    except IOError:
        current_configuration = {}
    return ConfigurationSchema().dump(current_configuration)


@configuration_api.route('/configuration', methods=['PUT', 'POST', 'PATCH'])
def update_configuration():
    request_data = request.get_json(force=True)
    new_configuration, errors = ConfigurationSchema().load(request_data)
    if errors:
        abort(401)

    dump_configuration(configuration=new_configuration)


def dump_configuration(configuration):
    with open(CONFIGURATION_PATH, str('wb')) as config_path:
        json.dump(configuration, config_path, indent=4)
