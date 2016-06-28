from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook
from headphones2.taggers.beets import identify_album_from_multiple_paths as beets_album_tag
from headphones2.taggers.acousid import identify_album_from_multiple_paths as acoustid_album_tag

logger = logbook.Logger(__name__)


def match_album(list_of_paths, use_acoustid=True, expected_artist=None, expected_album=None,
                expected_release_id=None):
    # type: (List[str], bool, str, str, str) -> album_info, track_mapping
    album_info, track_mapping = beets_album_tag(list_of_paths, expected_artist=expected_artist,
                                                expected_album=expected_album,
                                                expected_release_id=expected_release_id)
    if not album_info and use_acoustid:
        # try with acoustid
        release_id = acoustid_album_tag(list_of_paths, write_changes_to_items=False)
        if release_id:
            return match_album(list_of_paths, use_acoustid=False, expected_release_id=release_id)

    if not album_info and not use_acoustid:
        logger.error('Failed to match album, make sure that acoustID is enabled and available.')
        return None, None

    return album_info, track_mapping
