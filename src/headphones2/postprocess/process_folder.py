from __future__ import unicode_literals

import os

import logbook

from pathlib import Path
from beets.library import Item
from headphones2.postprocess.component_base import POST_PROCESSORS
from headphones2.postprocess.taggers.acoustid_tagger import AcoustIDAlbumTagger
from headphones2.postprocess.taggers.simple_tagger import SimpleBeetsTagger

logger = logbook.Logger()


def lookahead(iterable):
    it = iter(iterable)
    last = it.next()
    for val in it:
        yield last, False
        last = val
    yield last, True

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


def post_process_folder(folder):
    logger.info("Started post processing for {}".format(folder))
    logger.debug("Collecting media items from folders")
    items = [Item.from_path(str(f)) for f in FolderIterator(folder, extensions=['.mp3', '.flac'])]

    aid_tagger = AcoustIDAlbumTagger()
    beets_tagger = SimpleBeetsTagger()

    succeded, recommendation = aid_tagger.process(items)
    if succeded:
        beets_tagger.process(items, expected_release_id=recommendation)

    for processor in POST_PROCESSORS['extension']:
        processor.process(items)

    logger.info("Post processor compelted for {}".format(folder))


