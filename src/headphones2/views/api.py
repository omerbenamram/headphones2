import json
import datetime
import flask
import logbook

from flask import Blueprint, request, abort
import requests

from ..orm import *
from ..utils import get_artwork_for_album
from .cache import cache

logger = logbook.Logger(__name__)

api = Blueprint('api', __name__)

@api.route('/coverart/<string:rgid>/<string:size>')
@cache.cached()
def get_cover_art(rgid, size):
    """
    :param rgid: musicbrainz releasegroup_id
    :param size: large (500px) or small (250px)
    :return: binary jpeg
    """
    urls = get_artwork_for_album(rgid)
    if not urls:
        abort(404)

    chosen = urls.get(size)
    img = requests.get(chosen)
    if not img.ok:
        abort(404)

    resp = flask.make_response(img.content)
    resp.content_type = "image/jpeg"
    return resp


@api.route('/markAlbums')
def mark_albums():
    action = request.args['action']
    if action == 'WantedNew' or action == 'WantedLossless':
        action = 'Wanted'

    session = connect()

    album = session.query(Album).filter_by(id='bla').first()
    logger.info('Marking {} as {}'.format(album, action))
    album.status = action.lower()
    session.commit()

    # TODO: call 'search'


@api.route('/getLog')
def get_logs():
    return json.dumps({
        'iTotalDisplayRecords': 0,
        'iTotalRecords': 0,
        'aaData': [],
    })


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
        row = {
            "ArtistID": artist.id,
            "ArtistName": artist.name,
            "ArtistSortName": artist.name,
            "Status": artist.status,
            "TotalTracks": artist.total_tracks,
            "HaveTracks": artist.total_tracks > 0,  # TODO
            "LatestAlbum": "",
            "ReleaseDate": "",
            "ReleaseInFuture": "False",
            "AlbumID": "",
        }

        latest_album = artist.albums.join(Release).order_by(Release.release_date.desc()).first()
        latest_release = latest_album.releases.order_by(Release.release_date.desc()).first()
        if latest_album:
            row['ReleaseDate'] = latest_release.release_date
            row['LatestAlbum'] = latest_album.name
            row['AlbumID'] = latest_album.id
            if latest_release.release_date > datetime.dateime.today():
                row['ReleaseInFuture'] = "True"

        rows.append(row)

    result = {
        'iTotalDisplayRecords': len(rows),
        'iTotalRecords': totalcount,
        'aaData': rows,
    }

    return json.dumps(result)


