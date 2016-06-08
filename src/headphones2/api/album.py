import simplejson as json

from headphones2.orm import connect, Album

# TODO: DEPRECATED
class AlbumObject(object):
    pass
        # album_fields = {
        #     'id': fields.String,
        #     'name': fields.String,
        #     'status': fields.String,
        #     'total_tracks': fields.Integer,
        #     'possessed_tracks': fields.Integer,
        # }


class AlbumResource(object):
    pass
    # def get(self, album_id):
    #     session = connect()
    #     album = session.query(Album).filter_by(musicbrainz_id=album_id).first()
    #     album_json = json.dumps({
    #         'AlbumTitle': album.title,
    #         'ArtistName': album.artist.name,
    #         'Status': album.status.name
    #     })
    #     return album_json
