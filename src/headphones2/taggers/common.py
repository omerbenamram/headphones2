from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from collections import Counter
from itertools import chain

import musicbrainzngs

MAX_RELEASES = 5


def _select_best_release_from_many(results_list):
    """
    determines which releases the items have in common.
    also uses number of tracks to make sure its the same release
    :returns release_id or None
    """
    result_ids = chain.from_iterable(filter(None, [result.release_id for result in results_list]))
    top_matches = Counter(result_ids).most_common(MAX_RELEASES)
    actual_number_of_tracks = len(results_list)

    # check if number of tracks is the same
    for release_id, _ in top_matches:
        r = musicbrainzngs.get_release_by_id(release_id, includes='recordings')
        mediums = r['release']['medium-list']
        tracks = sum([medium['track-count'] for medium in mediums])
        if tracks == actual_number_of_tracks:
            return release_id

    return None
