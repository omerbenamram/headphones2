from gevent import monkey
from gevent.wsgi import WSGIServer

from app import app
from headphones2.tasks.engine import spin_consumers


def main():
    monkey.patch_all()

    with spin_consumers():
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()


if __name__ == "__main__":
    main()

