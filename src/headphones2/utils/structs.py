from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from collections import namedtuple


class AlbumAndTracksInfoTuple(namedtuple('AlbumAndTracksInfoTuple', ['album_info', 'items_to_track_info_mapping'])):
    pass


class FolderResult(namedtuple('AlbumItemsInfoTuple', ['folder_path', 'album_tracks_info_tuple'])):
    pass
