from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import py
import pytest

from beets.library import Item
from beets.dbcore import types
from headphones2.postprocess.process import pre_process_folder, post_process_album_task

from .conftest import vcr

Path = py.path.local

SAMPLE_DIR = Path(__file__).dirpath().join('fixtures').join('samples').join('album')


@pytest.fixture
def task(tmpdir):
    task = list(pre_process_folder(str(SAMPLE_DIR)))[0]
    for item in task:
        orig_path = Path(item.path)
        filename = orig_path.purebasename + orig_path.ext
        item.move_file(str(tmpdir.join(filename)), copy=True)
    return task


@pytest.fixture
def no_metadata_task(task):
    for item in task:
        for field, type in Item._fields.iteritems():
            if field != 'path':
                if type == types.STRING:
                    setattr(item, field, '')
                elif isinstance(type, types.PaddedInt):
                    setattr(item, field, 0)
        item.write()
    return task


@vcr.use_cassette()
def test_correctly_processes_task_with_metadata_and_no_hints(task, tmpdir):
    post_process_album_task(task, destination_folder=tmpdir)
    assert len(tmpdir.listdir()) > 0  # files were actually written to tmpdir


@vcr.use_cassette()
def test_correctly_processes_task_without_metadata(no_metadata_task, tmpdir):
    post_process_album_task(no_metadata_task, destination_folder=tmpdir)
    assert len(tmpdir.listdir()) > 0  # files were actually written to tmpdir
