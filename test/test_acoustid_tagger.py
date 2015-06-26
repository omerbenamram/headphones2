import pytest

from headphones2.postprocess.taggers.acoustid_tagger import AcoustIDAlbumTagger
from headphones2.postprocess.process import FolderIterator
from beets.library import Item
from conftest import vcr

HUMAN_EQUATION_MBID = '90392b89-77fc-3c39-813d-c5c09abf8943'
DARK_MEDICINE_ACOUSTID = 'f7c6418c-d8a7-46f8-bbeb-d5a11481776e'

@pytest.fixture
def single_item():
    track_22 = r"C:\Users\Omer\Desktop\The Theory of Everything [2013]\20 Ayreon - The Theory of Everything [2013] - Phase 2_ Symmetry, Dark Medicine.flac"
    item = Item.from_path(str(track_22))
    item.acoustid_id = ''
    item.acoustid_fingerprint = ''
    item.write()
    return item


@pytest.fixture
def album_item_list():
    folder = "M:\Ayreon\The Human Equation [2004]"
    items = [Item.from_path(str(p)) for p in FolderIterator(folder, extensions=['.mp3', '.flac'])]
    for item in items:
        item.acoustid_id = ''
        item.acoustid_fingerprint = ''
        item.write()
    return items


@vcr.use_cassette()
def test_acoust_id_tagger(single_item):
    tagger = AcoustIDAlbumTagger()
    tagger.process([single_item])

    assert single_item.acoustid_fingerprint
    assert single_item.acoustid_id == DARK_MEDICINE_ACOUSTID
