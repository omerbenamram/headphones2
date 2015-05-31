def album_to_dict(album):
    return {
        'AlbumID': album.musicbrainz_id,
        'ArtistName': album.artist.name,
        'ArtistID': album.artist.musicbrainz_id,
        'AlbumTitle': album.title,
        'ReleaseDate': album.releases.first().release_date,
        'Type': album.type,
        'Status': album.status
    }


def artist_to_dict(artist):
    return {
        'ArtistID': artist.musicbrainz_id,
        'ArtistName': artist.name,
        'Status': artist.status
    }
