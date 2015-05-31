import datetime
from headphones2.orm import *
from headphones2.utils import find_albums, musicbrainzngs, get_release_groups_for_artist, get_releases_for_release_group


def datetime_from_string(date_str):
    date = date_str.split('-')
    date += [1] * (3 - len(date))

    return datetime.datetime(*map(int, date))


def add_artist_to_db(artist_id, session):
    artist_info = musicbrainzngs.get_artist_by_id(artist_id)['artist']

    artist = Artist(name=artist_info['name'], musicbrainz_id=artist_id)
    session.add(artist)

    release_groups = get_release_groups_for_artist(artist.musicbrainz_id)

    for group_info in release_groups:
        album = Album(title=group_info['title'],
                      musicbrainz_id=group_info['id'],
                      type=group_info['type'],
                      artist=artist)
        session.add(album)

        releases = get_releases_for_release_group(album.musicbrainz_id)
        for release_info in releases:
            release = Release(
                musicbrainz_id=release_info['id'],
                release_date=datetime_from_string(release_info['date']),
                title=release_info['title'],
                asin=release_info.get('asin'),
                album=album)

            session.add(release)

            for media_info in release_info['medium-list']:
                media_number = media_info['position']
                for track_info in media_info['track-list']:
                    track = Track(
                        musicbrainz_id=track_info['id'],
                        length=track_info.get('length'),
                        media_number=media_number,
                        number=track_info['number'],
                        title=track_info['recording']['title'],
                        release=release
                    )
                    session.add(track)

    session.commit()