def album_to_dict(album):
    return {
        'AlbumID': album.id,
        'ArtistName': album.artist.name,
        'AlbumTitle': album.title,
        'ReleaseDate': album.releases.first().relase_date,
        'Type': album.type,
        'Status': album.status
    }
