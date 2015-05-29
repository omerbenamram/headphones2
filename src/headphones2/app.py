import os

from flask import Flask, send_file, send_from_directory

BUILD_PATH = os.path.abspath(os.path.join(__file__, '..', 'frontend', 'build'))

app = Flask(__name__, instance_path=os.path.dirname(__file__), static_folder=BUILD_PATH)
app.debug = True


@app.route('/')
def hello_word():
    return send_file(app.static_folder + '/index.html')


@app.route('/media/build/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder, path)


def main():
    app.run()


if __name__ == "__main__":
    main()
