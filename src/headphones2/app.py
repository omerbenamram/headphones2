import json
import os
import datetime

from flask import Flask, send_file, send_from_directory, render_template, request

from headphones2.orm.connector import connect
from headphones2.orm.media import Artist, Album, Release, Track
from headphones2.orm.serialize import album_to_dict
from headphones2.templates import serve_template

STATIC_PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'frontend'))

app = Flask(__name__, instance_path=os.path.dirname(__file__), static_folder=STATIC_PATH)
app.debug = True


@app.route('/')
def home():
    return serve_template('index.html', title='Home')


@app.route('/upcoming')
def upcoming():
    session = connect()
    upcoming_albums = session.query(Album).join(Release) \
        .filter(Release.release_date > datetime.datetime.today()) \
        .order_by(Release.release_date)
    wanted_albums = upcoming_albums.filter(Album.status == 'wanted')

    upcoming_data = []
    for album in upcoming_albums:
        upcoming_data.append(album_to_dict(album))

    wanted_data = []
    for album in wanted_albums:
        wanted_data.append(album_to_dict(album))

    return serve_template(templatename="upcoming.html", title="Upcoming", upcoming=upcoming_data, wanted=wanted_data)


@app.route('/getArtists.json')
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
            if latest_release.release_date > datetime.date.today():
                row['ReleaseInFuture'] = "True"

        rows.append(row)

    result = {
        'iTotalDisplayRecords': len(rows),
        'iTotalRecords': totalcount,
        'aaData': rows,
    }

    return json.dumps(result)


@app.route('/<path:path>')
def serv_static(path):
    return send_from_directory(app.static_folder, path)


def main():
    app.run()


if __name__ == "__main__":
    main()
