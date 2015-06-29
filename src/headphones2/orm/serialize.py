from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

def album_to_dict(album):
    return {
        'AlbumID': album.musicbrainz_id,
        'ArtistName': album.artist.name,
        'ArtistID': album.artist.musicbrainz_id,
        'AlbumTitle': album.title,
        'ReleaseDate': album.releases.first().release_date,
        'Type': album.type,
        'Status': album.status.name
    }


def artist_to_dict(artist):
    return {
        'ArtistID': artist.musicbrainz_id,
        'ArtistName': artist.name,
        'Status': artist.status.name
    }


def track_to_dict(track):
    return {
        'TrackNumber': track.number,
        'TrackTitle': track.title,
        'trackduration': track.length,
        'location' : track.location
    }