import os

from flask import Flask, send_file, send_from_directory, render_template

from headphones2.orm.connector import connect
from headphones2.orm.media import Artist, Album, Release, Track

BUILD_PATH = os.path.abspath(os.path.join(__file__, '..', 'frontend', 'interfaces', 'default'))

app = Flask(__name__, instance_path=os.path.dirname(__file__), static_folder=BUILD_PATH)
app.debug = True


@app.route('/')
def home():
    session = connect()
    artists = session.query(Artist.id.like('%'))
    return render_template(app.static_folder + '/index.html', artists=artists)


@app.route('/media/build/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder, path)


def main():
    app.run()


if __name__ == "__main__":
    main()
