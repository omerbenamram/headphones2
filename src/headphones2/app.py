from __future__ import (absolute_import, division, print_function, unicode_literals)

import os

import logbook
from flask import Flask, send_from_directory, send_file
from flask.ext.restful import Api
from pathlib import Path

from headphones2 import ArtistList, ArtistResource
from headphones2.tasks.engine import spin_consumers
from headphones2.views import pages, app_cache

FRONTEND_PATH = Path(__file__).parent.parent.joinpath("frontend")
BUILD_PATH = FRONTEND_PATH.joinpath("dist", "dev")
COMPONENTS_PATH = FRONTEND_PATH.joinpath("dist", "dev", "components")
ASSETS_PATH = FRONTEND_PATH.joinpath("dist", "dev", "assets")

app = Flask('headphones2', instance_path=os.path.abspath(os.path.dirname(__file__)), static_folder=str(BUILD_PATH))
app.debug = True

logger = logbook.Logger('headphones2.app')

app.register_blueprint(pages)
api = Api(app)
api.add_resource(ArtistList, str('/artists'), endpoint=str('artists'))
api.add_resource(ArtistResource, str('/artist/<artist_id>'), endpoint=str('artist'))
app_cache.init_app(app)


@app.route('/')
@app.route('/home')
def home():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/components/<path:path>')
def serve_static(path):
    return send_from_directory(str(COMPONENTS_PATH), path)


@app.route('/assets/<path:path>')
def serve_asset(path):
    return send_from_directory(str(ASSETS_PATH), path)


@app.route('/<path:path>')
def serve_component(path):
    return send_from_directory(str(FRONTEND_PATH), path)


@app.route('/app/bootstrap.js')
def serve_bootstrap():
    return send_file(str(BUILD_PATH.joinpath('bootstrap.js')))


def main():
    with spin_consumers():
        app.run()


if __name__ == "__main__":
    main()
