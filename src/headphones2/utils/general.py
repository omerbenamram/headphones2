from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import datetime
import os
import re
import sys
from flask import request
from headphones2.configuration import MEDIA_FORMATS

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


def is_media_file(path):
    """
    A simple check if a file extension is a known media format
    :param path: path
    :return:
    """
    return os.path.splitext(path)[1][1:] in MEDIA_FORMATS


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return path + args


def datetime_from_string(date_str):
    date = date_str.split('-')
    date += [1] * (3 - len(date))

    return datetime.datetime(*map(int, date))