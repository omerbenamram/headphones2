from __future__ import unicode_literals, absolute_import, print_function, division

from flask.ext.restful import fields, Resource, marshal, reqparse
from werkzeug.utils import redirect

from headphones2.orm import Artist, Track, Release, Album, connect
from headphones2.tasks import add_artist_task

parser = reqparse.RequestParser()
parser.add_argument('artist_id')


class ArtistListObject(object):
    artist_list_fields = {
        'id': fields.String,
        'name': fields.String,
        'status': fields.String,
        'total_tracks': fields.Integer,
        'possessed_tracks': fields.Integer,
        'latest_album': fields.String,
        'latest_album_release_date': fields.DateTime,
        'latest_album_id': fields.String
    }

    def __init__(self, artist_id, name, status, total_tracks, possessed_tracks,
                 latest_album, latest_album_release_date, latest_album_id):
        self.id = artist_id
        self.name = name
        self.status = status
        self.total_tracks = total_tracks
        self.possessed_tracks = possessed_tracks
        self.latest_album = latest_album
        self.latest_album_release_date = latest_album_release_date
        self.latest_album_id = latest_album_id


class ArtistList(Resource):
    def get(self):
        session = connect()
        artists = session.query(Artist)

        rows = []
        for artist in artists:
            total_tracks = session.query(Track) \
                .join(Release) \
                .join(Album) \
                .join(Artist) \
                .filter(Release.is_selected, Artist.musicbrainz_id == artist.musicbrainz_id).count()

            possessed_tracks_count = 0

            latest_album = artist.albums.join(Release).order_by(Release.release_date.desc()).first()

            if latest_album:
                latest_release = latest_album.releases.order_by(Release.release_date.desc()).first()
                release_date = latest_release.release_date
                latest_album_id = latest_album.musicbrainz_id
            else:
                release_date, latest_album_id = None, None

            row = ArtistListObject(artist.musicbrainz_id,
                                   artist.name,
                                   artist.status.name,
                                   total_tracks,
                                   possessed_tracks_count,
                                   latest_album.title,
                                   release_date,
                                   latest_album_id)

            rows.append(marshal(row, ArtistListObject.artist_list_fields))

        return rows

    def post(self):
        args = parser.parse_args()
        artist_id = args.get('artist_id')
        if not artist_id:
            return 500

        add_artist_task(artist_id=artist_id)
        return 200


class ArtistResource(Resource):
    def delete(self, artist_id):
        session = connect()
        artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()
        session.delete(artist)
        session.commit()
        return redirect('/home')
