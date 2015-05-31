import os
import headphones2
from flask.ext.cache import Cache

CACHE_DIR = os.path.abspath(os.path.join(headphones2.__path__[0], '..', '..', 'cache'))

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

cache = Cache(config={'CACHE_TYPE': 'filesystem',
                      'CACHE_DIR': CACHE_DIR,
                      'CACHE_THRESHOLD': '1000'})

