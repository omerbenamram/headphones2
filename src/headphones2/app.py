import os

from flask import Flask, send_file, send_from_directory, render_template

from headphones2.orm.connector import connect
from headphones2.orm.media import Artist, Album, Release, Track
from headphones2.templates import serve_template

STATIC_PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'frontend'))

app = Flask(__name__, instance_path=os.path.dirname(__file__), static_folder=STATIC_PATH)
app.debug = True


@app.route('/')
def home():
    session = connect()
    artists = session.query(Artist.id.like('%'))
    return serve_template('index.html', title='Home', artists=artists)


@app.route('/<path:path>')
def serv_static(path):
    return send_from_directory(app.static_folder, path)


def main():
    app.run()


if __name__ == "__main__":
    main()
