from __future__ import (absolute_import, division, print_function, unicode_literals)

from contextlib import closing
from datetime import datetime

import logbook
import musicbrainzngs
from beets.autotag import AlbumInfo
from beets.autotag import TrackInfo
from headphones2.exceptions import HeadphonesException
from headphones2.external.musicbrainz import get_release_groups_for_artist, get_releases_for_release_group, \
    musicbrainz_lock
from headphones2.orm import Artist, Status, Album, Release, Track

from .engine import huey
from ..orm import connect

logger = logbook.Logger(__name__)


@huey.task()
def add_artist_task(artist_id):
    with closing(connect()) as session:
        add_artist_to_db(artist_id, session)


@huey.task()
def add_release_task(release_id):
    with closing(connect()) as session:
        # TODO: implement
        raise NotImplementedError


def add_artist_to_db(artist_id, session):
    # type: (six.stringtypes, Any) -> None
    """
    Adds an artist to the db
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
        logger.debug('found {type} {name}'.format(type=group_info['type'], name=group_info['title']))
        album = Album(title=group_info['title'],
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
        title=release_info.album,
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
            title=track_info.title,
            release=release
        )
        session.add(track)

    return release
