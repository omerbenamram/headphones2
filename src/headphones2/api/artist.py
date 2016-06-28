from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import flask
from flask import Blueprint, jsonify
from werkzeug.utils import redirect

from headphones2.orm import Artist, Track, Release, Album, connect
from headphones2.tasks import add_artist_task

artist_api = Blueprint('artist_api', __name__, url_prefix='/api')


@artist_api.route('/artists', methods=['GET'])
def get_artists():
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
            latest_album_title = latest_album.title
            latest_release = latest_album.releases.order_by(Release.release_date.desc()).first()
            latest_album_release_date = latest_release.release_date
            latest_album_id = latest_album.musicbrainz_id
        else:
            latest_album_title, latest_album_release_date, latest_album_id = None, None, None

        rows.append({
            'id': artist.musicbrainz_id,
            'name': artist.name,
            'status': artist.status.name,
            'total_tracks': total_tracks,
            'possessed_tracks': 0,  # TODO: implement
            'latest_album': latest_album_title,
            'latest_album_release_date': latest_album_release_date,
            'latest_album_id': latest_album_id
        })

    return jsonify({
        'data': rows
    })


@artist_api.route('/artists', methods=['POST'])
def add_artist():
    args = flask.request.args
    artist_id = args.get('artist_id')
    if not artist_id:
        flask.abort(422)  # Missing HTTP Arguments

    add_artist_task(artist_id=artist_id)
    return 200


@artist_api.route('/artists/<string:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    session = connect()
    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).first()
    session.delete(artist)
    session.commit()
    return redirect('/home')
