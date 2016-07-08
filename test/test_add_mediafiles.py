from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from headphones2.tasks import add_track_mapping_to_db
from headphones2.utils.structs import AlbumAndTracksInfoTuple

from .conftest import *
from .fixtures import *
from headphones2.orm import *


@vcr.use_cassette()
def test_add_media_files_to_db(session_with_artist, folder_info):
    # type: (Session, FolderResult) -> None

    UNIVERSAL_MIGRATOR_RELEASE_ID = '6161bcee-1837-3f92-8627-f865a5896613'
    session = session_with_artist

    _, album_and_track_info_tuple = folder_info  # type: str, AlbumAndTracksInfoTuple

    add_track_mapping_to_db(album_and_track_info_tuple.album_info,
                            album_and_track_info_tuple.items_to_track_info_mapping,
                            session)

    files = session.query(MediaFile).join(Release).filter(Release.musicbrainz_id == UNIVERSAL_MIGRATOR_RELEASE_ID).all()

    assert files
    assert len(files) == 11
