from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import contextlib
import multiprocessing

from huey import Huey
from huey.consumer import Consumer

NUM_OF_CONSUMER_PROCESSES = 2
SQLITE_TASK_DB_PATH = r'C:\temp\tasks.db'
USE_REDIS = True

if USE_REDIS:
    # Requiers a redis-server instance.
    # On windows: redis-server.exe --maxheap 30mb
    from huey import RedisHuey

    huey = RedisHuey('task-queue', 'localhost:6379')

else:
    # Sqlite is limited to one consumer per db.
    NUM_OF_CONSUMER_PROCESSES = 1
    from huey.backends.sqlite_backend import SqliteQueue, SqliteDataStore

    result_store = SqliteDataStore('results', SQLITE_TASK_DB_PATH)
    queue = SqliteQueue('task_queue', SQLITE_TASK_DB_PATH)
    huey = Huey(queue, result_store=result_store)


def _run_consumer():
    consumer = Consumer(huey)
    consumer.run()


@contextlib.contextmanager
def spin_consumers():
    # Manual consumer can be lunched by running:
    # huey_consumer.py headphones2.tasks.huey

    consumers = []
    for _ in xrange(NUM_OF_CONSUMER_PROCESSES):
        proc = multiprocessing.Process(target=_run_consumer)
        proc.start()

        consumers.append(proc)

    yield

    for proc in consumers:
        proc.join()
