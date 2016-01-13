"""
A blueprint for all the 'pages' in the system (e.g, home, wanted, extras, etc).
"""
from .api import api
from .pages import pages

from .cache import cache as app_cache
