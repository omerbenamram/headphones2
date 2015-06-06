import pytest

from headphones2.media.acoustid_tagger import Task, AcoustIDAlbumTagger
from headphones2.media.process_folder import FolderIterator
from beets.library import Item
from conftest import vcr

HUMAN_EQUATION_MBID = '90392b89-77fc-3c39-813d-c5c09abf8943'


@pytest.fixture
def album_task():
    folder = "M:\Ayreon\The Human Equation [2004]"
    item_objects = [Item.from_path(str(p)) for p in FolderIterator(folder, extensions=['.mp3', '.flac'])]
    return Task(item_objects)


@vcr.use_cassette()
def test_acoust_id_tagger(album_task):
    tagger = AcoustIDAlbumTagger(album_task)
    tagger.tag()
    assert HUMAN_EQUATION_MBID in tagger.results
