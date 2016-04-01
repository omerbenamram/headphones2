from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

import simplejson as json
import sys
from flask.ext.restful import Resource, fields, marshal, reqparse, abort

# noinspection PyUnresolvedReferences
from pies.overrides import *
from headphones2.config import CONFIGURATION_PATH
import logbook

logger = logbook.Logger(level=logbook.DEBUG)
logger.handlers.append(logbook.StreamHandler(sys.stdout))

configuration_fields = {
    'libraryPath': fields.String,
    'debug': fields.Boolean
}

parser = reqparse.RequestParser()
parser.add_argument('libraryPath')

try:
    with open(CONFIGURATION_PATH, str('rb')) as fp:
        CONFIGURATION = marshal(json.load(fp), configuration_fields)
except IOError:
    # No configuration available
    CONFIGURATION = {}


class ConfigurationResource(Resource):
    def get(self):
        return marshal(CONFIGURATION, configuration_fields)

    def put(self):
        args = parser.parse_args()
        path = args['libraryPath']
        logger.debug(path)
        path_valid = verify_path_input(path)
        if not path_valid:
            abort(412)

        CONFIGURATION['libraryPath'] = path
        dump_configuration()


def dump_configuration():
    with open(CONFIGURATION_PATH, str('wb')) as config_path:
        json.dump(marshal(CONFIGURATION, configuration_fields), config_path, indent=4)


def verify_path_input(path_input):
    return os.path.isdir(path_input.strip("'"))
