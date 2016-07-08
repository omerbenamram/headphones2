from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import time

from contextlib import closing
from datetime import datetime

import logbook
import musicbrainzngs
import six
from beets.autotag import AlbumInfo
from beets.autotag import TrackInfo
from beets.importer import albums_in_dir
from headphones2.exceptions import HeadphonesException
from headphones2.external.musicbrainz import get_release_groups_for_artist, get_releases_for_release_group, \
    musicbrainz_lock
from headphones2.orm import Artist, Status, Album, Release, Track, MediaFile
from headphones2.taggers.pipeline import match_album_from_list_of_paths
from headphones2.utils.general import ensure_unicode
from headphones2.utils.structs import FolderResult
from redis.lock import Lock

from .engine import huey, local_redis
from ..orm import connect

logger = logbook.Logger(__name__)

write_lock = Lock(local_redis, name='sqlite_write')


@huey.task()
def add_artist_task(artist_id):
    with closing(connect()) as session:
        already_working = local_redis.setnx(artist_id, 'in_progress')
        if already_working == 1:
            add_artist_to_db(artist_id, session)
            local_redis.delete(artist_id)
            return True
        else:
            logger.debug('Task for adding artist {} already in progress'.format(artist_id))
            return False


@huey.task()
def add_album_from_folder_to_db(album_and_track_info_tuple, artist_id):
    with closing(connect()) as session:
        artist = session.query(Artist).filter(Artist.musicbrainz_id == artist_id).first()

        if not artist:
            # maybe still in progress
            while not artist:
                in_progress = local_redis.get(artist_id)
                if in_progress:
                    logger.debug('Still Waiting for artist {} to be added to DB'.format(artist_id))
                    time.sleep(5)
                else:
                    break

        add_track_mapping_to_db(album_and_track_info_tuple.album_info,
                                album_and_track_info_tuple.items_to_track_info_mapping,
                                session)


def add_artist_to_db(artist_id, session):
    # type: (six.stringtypes, Any) -> None
    """
    Adds an artist to the db, including all album and tracks information
    :param artist_id: musicbrainzid
    :type artist_id: str
    :param session: valid SQLAlchemy Session
    :return: None
    """
    logger.info('adding artist {} to db'.format(artist_id))
    with musicbrainz_lock:
        artist_info = musicbrainzngs.get_artist_by_id(artist_id)['artist']

    artist = Artist(name=artist_info['name'],
                    musicbrainz_id=artist_id,
                    status=Status.Wanted)
    session.add(artist)

    release_groups = get_release_groups_for_artist(artist.musicbrainz_id)

    for group_info in release_groups:
        logger.debug('found {type} {name}'.format(type=group_info['type'], name=ensure_unicode(group_info['title'])))
        album = Album(title=ensure_unicode(group_info['title']),
                      musicbrainz_id=group_info['id'],
                      type=group_info['type'],
                      artist=artist,
                      status=Status.Wanted
                      )

        session.add(album)

        releases = get_releases_for_release_group(album.musicbrainz_id)
        for release_info in releases:
            add_album_and_tracks_to_db(album, release_info, session)

        # Chose oldest release (it's usually the original release)
        chosen_release = session.query(Release).join(Album).filter(Album.musicbrainz_id == group_info['id']).order_by(
            Release.release_date.asc()).first()
        if chosen_release:
            chosen_release.is_selected = True

    with write_lock:
        session.commit()


def add_album_and_tracks_to_db(album, release_info, session):
    # type: (Album, AlbumInfo, Any) -> Release

    # will default to 2014-1-1 if no month or date for example.
    available_date_info = {attr: getattr(release_info, attr) or 1 for attr in ('year', 'month', 'day')}

    if not available_date_info:
        raise HeadphonesException('Cannot get release date for release {}'.format(release_info.album))

    release_date = datetime(**available_date_info)

    release_info.decode()

    release = Release(
        musicbrainz_id=release_info.album_id,
        release_date=release_date,
        title=ensure_unicode(release_info.album),
        asin=release_info.asin,
        country=release_info.country,
        album=album)

    session.add(release)

    for track_info in release_info.tracks:  # type: TrackInfo
        track_info.decode()
        track = Track(
            musicbrainz_id=track_info.track_id,
            length=track_info.length,
            media_number=track_info.medium_index,
            number=track_info.index,
            title=ensure_unicode(track_info.title),
            release=release
        )
        session.add(track)

    return release


def add_track_mapping_to_db(album_info, items_to_trackinfo_mapping, session):
    # type: (AlbumInfo, Dict[Item, TrackInfo], Session) -> None
    """
    Adds track mapping to DB, assumes artist exist in DB.
    :param album_info: beets AlbumInfo object
    :param session: A Valid SQLAlchemy Session
    :param items_to_trackinfo_mapping: A mapping of library items to TrackInfo
    :return:
    """
    first_trackinfo = items_to_trackinfo_mapping.values()[0]  # type: TrackInfo
    artist_id = first_trackinfo.artist_id

    assert session.query(Artist).filter_by(musicbrainz_id=artist_id).first() \
        , 'Artist {} does not yet exist in DB! Cannot add tracks'.format(artist_id)

    for item, trackinfo in six.iteritems(items_to_trackinfo_mapping):
        assert trackinfo.track_id

        track = session.query(Track).filter_by(musicbrainz_id=trackinfo.track_id).first()
        assert track, "Track {} does not exist in DB!".format(item.mb_trackid)

        assert album_info.album_id
        release = session.query(Release).filter_by(musicbrainz_id=album_info.album_id).first()
        assert release, "Release {} does not exist in DB!".format(album_info.album_id)

        # path has to be unicode
        path = ensure_unicode(item.path)

        mf = MediaFile(path=path,
                       format=os.path.splitext(path)[1],
                       track=track,
                       release=release)

        session.add(mf)

    with write_lock:
        session.commit()


def fetch_albums_from_root_directory(root_path):
    results = [FolderResult(folder, match_album_from_list_of_paths(list_of_files)) for folder, list_of_files in
               list(albums_in_dir(root_path))]
    return results
