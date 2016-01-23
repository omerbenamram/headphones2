from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import stat

from pies.overrides import *

from headphones2.utils.general import get_filesystem_encoding, filename_to_ui


class Path(object):
    """
    :param exists: if set to true, the file or directory needs to exist for
                   this value to be valid.  If this is not required and a
                   file does indeed not exist, then all further checks are
                   silently skipped.
    :param file_okay: controls if a file is a possible value.
    :param dir_okay: controls if a directory is a possible value.
    :param writable: if true, a writable check is performed.
    :param readable: if true, a readable check is performed.
    :param resolve_path: if this is true, then the path is fully resolved
                         before the value is passed onwards.  This means
                         that it's absolute and symlinks are resolved.
    :param allow_dash: If this is set to `True`, a single dash to indicate
                       standard streams is permitted.
    """
    envvar_list_splitter = os.path.pathsep

    def __init__(self, exists=False, file_okay=True, dir_okay=True,
                 writable=False, readable=True, resolve_path=False,
                 allow_dash=False, path_type=None):
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.writable = writable
        self.readable = readable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.type = path_type

        if self.file_okay and not self.dir_okay:
            self.name = 'file'
            self.path_type = 'File'
        if self.dir_okay and not self.file_okay:
            self.name = 'directory'
            self.path_type = 'Directory'
        else:
            self.name = 'path'
            self.path_type = 'Path'

    def coerce_path_result(self, rv):
        if self.type is not None and not isinstance(rv, self.type):
            if isinstance(self.type, str):
                rv = rv.decode(get_filesystem_encoding())
            else:
                rv = rv.encode(get_filesystem_encoding())
        return rv

    def fail(self, message):
        raise ValueError(message)

    def convert(self, value):
        rv = value

        is_dash = self.file_okay and self.allow_dash and rv in (b'-', '-')

        if not is_dash:
            if self.resolve_path:
                rv = os.path.realpath(rv)

            try:
                st = os.stat(rv)
            except OSError:
                if not self.exists:
                    return self.coerce_path_result(rv)
                self.fail('%s "%s" does not exist.' % (
                    self.path_type,
                    filename_to_ui(value)
                ))

        if not self.file_okay and stat.S_ISREG(st.st_mode):
            self.fail('%s "%s" is a file.' % (
                self.path_type,
                filename_to_ui(value)
            ))
        if not self.dir_okay and stat.S_ISDIR(st.st_mode):
            self.fail('%s "%s" is a directory.' % (
                self.path_type,
                filename_to_ui(value)
            ))
        if self.writable and not os.access(value, os.W_OK):
            self.fail('%s "%s" is not writable.' % (
                self.path_type,
                filename_to_ui(value)
            ))
        if self.readable and not os.access(value, os.R_OK):
            self.fail('%s "%s" is not readable.' % (
                self.path_type,
                filename_to_ui(value)
            ))

        return self.coerce_path_result(rv)
