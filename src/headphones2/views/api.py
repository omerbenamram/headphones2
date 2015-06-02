import json
import datetime

import flask
import logbook

from flask import Blueprint, request, abort
import requests
from headphones2.tasks.musicbrainz import get_artwork_for_album_task

from ..orm import *
from headphones2.external.lastfm import lastfm_api_wrapper
from headphones2.external.musicbrainz import get_artwork_for_album
from .cache import cache

logger = logbook.Logger(__name__)

api = Blueprint('api', __name__)


@api.route('/artwork/album/<string:rgid>/<string:size>')
@cache.cached()
def get_album_cover_art(rgid, size='small'):
    """
    :param rgid: musicbrainz releasegroup_id
    :param size: large (500px) or small (250px)
    :return: binary jpeg
    """
    urls = get_artwork_for_album_task(rgid).get(True)
    if not urls:
        abort(404)

    chosen = urls.get(size)
    img = requests.get(chosen)
    if not img.ok:
        abort(404)

    resp = flask.make_response(img.content)
    resp.content_type = "image/jpeg"
    return resp


@api.route('/artwork/artist/<string:mbid>/<string:size>')
@cache.cached()
def get_artist_artwork(mbid, size='small'):
    """
    :param mbid: musicbrainz artist_id
    :param size: large (500px) or small (250px)
    :return: binary jpeg
    """
    artist_info = lastfm_api_wrapper("artist.getinfo", mbid=mbid)
    if not artist_info:
        abort(404)

    artist_artwork = artist_info['artist']['image']
    # convert response list of dicts to something more usable
    size_dict = {d['size']: d['#text'] for d in artist_artwork}
    img = requests.get(size_dict[size])

    if not img.ok:
        abort(404)

    resp = flask.make_response(img.content)
    resp.content_type = "image/jpeg"
    return resp


@api.route('/markAlbums')
def mark_albums():
    request_args = dict(request.args)
    action = request_args.pop('action')[0]
    artist_id = request_args.pop('ArtistID')[0]

    if action == 'WantedNew' or action == 'WantedLossless':
        action = 'Wanted'

    session = connect()

    for album_id, on_or_off in request_args.items():
        album = session.query(Album).filter_by(musicbrainz_id=album_id).one()
        if on_or_off == ['on']:
            logger.info('Marking {} as {}'.format(album, action))
            album.status = Status.from_name(action)

    session.commit()

    # TODO: call 'search'

    return ''


@api.route('/getLog')
def get_logs():
    return json.dumps({
        'iTotalDisplayRecords': 0,
        'iTotalRecords': 0,
        'aaData': [],
    })


@api.route('/getAlbumjson')
def get_album():
    album_id = request.args['AlbumID']
    session = connect()
    album = session.query(Album).filter_by(musicbrainz_id=album_id).first()
    album_json = json.dumps({
        'AlbumTitle': album.title,
        'ArtistName': album.artist.name,
        'Status': album.status.name
    })
    return album_json


@api.route('/getArtists.json')
def get_artists():
    display_start = int(request.args.get('iDisplayStart', '0'))
    display_length = int(request.args.get('iDisplayLength', '100'))
    search_query = request.args.get('sSearch', '')
    sort_column = request.args.get('iSortCol_0', '')
    is_sort_asc = request.args.get('sSortDir_0', 'asc') == 'asc'

    session = connect()
    query = session.query(Artist)

    if sort_column == '2':
        # Status column.
        if is_sort_asc:
            query = query.order_by(Artist.status.asc())
        else:
            query = query.order_by(Artist.status.desc())
    elif sort_column == '3':
        # Release Date column.
        query = query.join(Album).join(Release)
        if is_sort_asc:
            query = query.order_by(Release.release_date.asc())
        else:
            query = query.order_by(Release.release_date.desc())
    elif sort_column == '4':
        sortbyhavepercent = True

    if search_query:
        query = query.filter(Artist.name.ilike('%{}%'.format(search_query)))

    totalcount = query.count()

    artists = query[display_start:display_start + display_length]
    rows = []
    for artist in artists:
        # TODO: Don't count tracks in each release multiple times..
        total_tracks = sum([release.tracks.count() for album in artist.albums for release in album.releases])
        row = {
            "ArtistID": artist.musicbrainz_id,
            "ArtistName": artist.name,
            "ArtistSortName": artist.name,
            "Status": artist.status.name,
            "TotalTracks": total_tracks,
            "HaveTracks": total_tracks > 0,  # TODO
            "LatestAlbum": "",
            "ReleaseDate": "",
            "ReleaseInFuture": "False",
            "AlbumID": "",
        }

        latest_album = artist.albums.join(Release).order_by(Release.release_date.desc()).first()
        if latest_album:
            latest_release = latest_album.releases.order_by(Release.release_date.desc()).first()
            row['ReleaseDate'] = latest_release.release_date.isoformat()
            row['LatestAlbum'] = latest_album.title
            row['AlbumID'] = latest_album.id
            if latest_release.release_date > datetime.datetime.today():
                row['ReleaseInFuture'] = "True"

        rows.append(row)

    result = {
        'iTotalDisplayRecords': len(rows),
        'iTotalRecords': totalcount,
        'aaData': rows,
    }

    return json.dumps(result)
