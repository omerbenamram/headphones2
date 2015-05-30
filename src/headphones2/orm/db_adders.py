from headphones2.orm import connect
from headphones2.orm.media import Artist, Album
from headphones2.utils import find_artist_by_name, find_albums

AYREON_ID = '7bbfd77c-1102-4831-9ba8-246fb67460b3'

def add_artist(name,musicbrainz_id):
    session = connect()
    artist = Artist(name=name, musicbrainz_id=musicbrainz_id)
    session.add(artist)
    session.commit()

def add_album(title, musicbrainz_id, album_type, artist_object):
    artist_id = artist_object.id
    album = Album(title=title, musicbrainz_id=musicbrainz_id, type=album_type,artist_id=artist_id)
    session.add(album)
    session.commit()

session = connect()
a = find_albums('The Theory of Everything', artist_id=AYREON_ID)[0]
ayreon = session.query(Artist).filter_by(musicbrainz_id = AYREON_ID)[0]
add_album(a['title'], a['id'], a['type'], ayreon)


#ayreon = find_artist_by_name('Ayreon')[0]
#add_artist(ayreon['name'],ayreon['id'])__author__ = 'Omer'
