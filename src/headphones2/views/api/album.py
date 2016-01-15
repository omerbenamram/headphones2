from flask.ext.restful import Resource, fields

from headphones2.orm import connect, Album


class AlbumObject(object):
    album_fields = {
        'id': fields.String,
        'name': fields.String,
        'status': fields.String,
        'total_tracks': fields.Integer,
        'possessed_tracks': fields.Integer,
    }


class AlbumResource(Resource):
    def get(self, album_id):
        session = connect()
        album = session.query(Album).filter_by(musicbrainz_id=album_id).first()
        album_json = json.dumps({
            'AlbumTitle': album.title,
            'ArtistName': album.artist.name,
            'Status': album.status.name
        })
        return album_json
