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
