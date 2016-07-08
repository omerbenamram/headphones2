from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import contextlib
import logging
import multiprocessing

import sys

import redis
from headphones2.configuration import DEFAULT_LOG_PATH
from huey.consumer import Consumer

NUM_OF_CONSUMER_PROCESSES = 2
# Requiers a redis-server instance.
# On windows: redis-server.exe --maxheap 30mb


from huey import RedisHuey

local_redis = redis.Redis()
huey = RedisHuey('task-queue')


def _run_consumer():
    consumer = Consumer(huey)
    consumer._logger.addHandler(logging.FileHandler(DEFAULT_LOG_PATH))
    consumer._logger.addHandler(logging.StreamHandler(sys.stdout))
    consumer.run()


@contextlib.contextmanager
def spin_consumers():
    # Manual consumer can be lunched by running:
    # huey_consumer.py headphones2.tasks.huey

    consumers = []
    for _ in range(NUM_OF_CONSUMER_PROCESSES):
        proc = multiprocessing.Process(target=_run_consumer)
        proc.start()

        consumers.append(proc)

    yield

    for proc in consumers:
        proc.join()
