import os

from flask import Flask, send_from_directory
import logbook
from headphones2.tasks.engine import spin_consumers
from headphones2.views import pages, api, cache
from wdb.ext import WdbMiddleware

STATIC_PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'frontend'))

app = Flask('headphones2', instance_path=os.path.dirname(__file__), static_folder=STATIC_PATH)
app.debug = True

logger = logbook.Logger('headphones2.app')

app.register_blueprint(pages)
app.register_blueprint(api)

app.wsgi_app = WdbMiddleware(app.wsgi_app)
cache.init_app(app)


@app.route('/<path:path>')
def serv_static(path):
    return send_from_directory(app.static_folder, path)


def main():
    with spin_consumers():
        app.run(use_debugger=False)


if __name__ == "__main__":
    main()
