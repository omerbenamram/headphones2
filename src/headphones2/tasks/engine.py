import contextlib
import multiprocessing

from huey import Huey
from huey.consumer import Consumer


if True:
    # Requiers a redis-server instance.
    # On windows: redis-server.exe --maxheap 30mb
    from huey.backends.redis_backend import RedisQueue, RedisDataStore

    queue = RedisQueue('task-queue')
    result_store = RedisDataStore('results')
else:
    # Sqlite is limited to one consumer per db.
    from huey.backends.sqlite_backend import SqliteQueue, SqliteDataStore

    result_store = SqliteDataStore('results')
    queue = SqliteQueue('task_queue', r'C:\ohad\workspace\tasks.db')

huey = Huey(queue, result_store=result_store)


def _run_consumer():
    consumer = Consumer(huey)
    consumer.run()


@contextlib.contextmanager
def spin_consumers():
    # Manual consumer can be lunched by running:
    # huey_consumer.py headphones2.tasks.huey

    consumers = []
    for _ in xrange(0):
        proc = multiprocessing.Process(target=_run_consumer)
        proc.start()

        consumers.append(proc)

    yield

    for proc in consumers:
        proc.join()