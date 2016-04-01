from __future__ import (absolute_import, division, print_function, unicode_literals)

import os

import logbook
from flask import Flask, send_from_directory

from headphones2.tasks.engine import spin_consumers
from headphones2.views import pages
from headphones2.api import artist_api, artwork_api

FRONTEND_PATH = os.path.join(__file__, os.pardir, os.pardir, 'frontend')
BUILD_PATH = os.path.join(FRONTEND_PATH, "dist")
ASSETS_PATH = os.path.join(FRONTEND_PATH, "dist", "assets")

app = Flask('headphones2', static_folder=str(BUILD_PATH))
app.debug = True

logger = logbook.Logger('headphones2.app')

app.register_blueprint(pages)
app.register_blueprint(artist_api)
app.register_blueprint(artwork_api)


@app.route('/')
@app.route('/home')
def home():
    return send_from_directory(os.path.join(FRONTEND_PATH, 'dist', 'index.html'))


@app.route('/assets/<path:path>')
def serve_asset(path):
    return send_from_directory(str(ASSETS_PATH), path)


@app.route('/<path:path>')
def serve_component(path):
    return send_from_directory(str(FRONTEND_PATH), path)


def main():
    with spin_consumers():
        app.run()


if __name__ == "__main__":
    main()
