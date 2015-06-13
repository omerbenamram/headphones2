import os

import logbook

from pathlib import Path
from beets.library import Item
from component_base import POST_PROCESSORS, PostProcessorException

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
    items = [Item.from_path(str(f)) for f in FolderIterator(folder)]
    taggers = POST_PROCESSORS['tagger']
    for processor, is_last in lookahead(taggers):
        try:
            logger.debug("Calling post processor {}".format(processor))
            processor.process(items)
        except PostProcessorException:
            if is_last:
                raise "Could not tag media in folder {}".format(folder)
            continue

    for processor in POST_PROCESSORS['extension']:
        processor.process(items)

    logger.info("Post processor compelted for {}".format(folder))
