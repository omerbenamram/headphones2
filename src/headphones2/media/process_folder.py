import os

from beets.library import Item
from beets.autotag.match import tag_album, Recommendation
from beetsplug.chroma import acoustid_match
import logbook

logger = logbook.Logger()

from pathlib import Path

class FolderIterator(object):
    """
    iter container for media files in folder - recursively
    """

    def __init__(self, folder, extensions=()):
        assert os.path.isdir(folder), "Cannot instantiate without folder"
        self.folder = folder
        self.extensions = [x.lower() for x in extensions]

    def __iter__(self):
        for root, dirs, files in os.walk(self.folder):
            for p in [Path(x) for x in files]:
                if not self.extensions:
                    yield Path(root).joinpath(p)
                # avoid mess with files without suffixes being matched
                if p.suffix and p.suffix in self.extensions:
                    yield Path(root).joinpath(p)


def match_album(folder, match_artist_id='', match_album_id=''):
    item_objects = [Item.from_path(str(p)) for p in FolderIterator(folder, extensions=['.mp3', '.flac'])]

    acoustid_matches = []
    for item in (p.__str__() for p in FolderIterator(folder, extensions=['.mp3', '.flac'])):
        acoustid_matches.append(acoustid_match(logger, item))

    artist_name, album_name, album_recommendation_list, recommendation = \
        tag_album(item_objects, search_artist=match_artist_id, search_album=match_album_id)

    # recommendation system is very strage, might just take first album regardless since tagging is excellent.
    if recommendation is not Recommendation.none:
        return album_recommendation_list[0].album_id

    return None
