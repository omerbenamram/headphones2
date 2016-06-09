import re
import sys
from flask import request

PY2 = sys.version_info[0] == 2
WIN = sys.platform.startswith('win')
DEFAULT_COLUMNS = 80

_ansi_re = re.compile('\033\[((?:\d|;)*)([a-zA-Z])')


def get_filesystem_encoding():
    return sys.getfilesystemencoding() or sys.getdefaultencoding()


def filename_to_ui(value):
    if isinstance(value, bytes):
        value = value.decode(get_filesystem_encoding(), 'replace')
    else:
        value = value.encode('utf-8', 'surrogateescape') \
            .decode('utf-8', 'replace')
    return value


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return path + args
