import json
import os
import datetime

from flask import Flask, send_file, send_from_directory, render_template, request

from headphones2.orm.connector import connect
from headphones2.orm.media import Artist, Album, Release, Track
from headphones2.templates import serve_template

STATIC_PATH = os.path.abspath(os.path.join(__file__, '..', '..', 'frontend'))

app = Flask(__name__, instance_path=os.path.dirname(__file__), static_folder=STATIC_PATH)
app.debug = True


@app.route('/')
def home():
    session = connect()
    artists = session.query(Artist.id.like('%'))
    return serve_template('index.html', title='Home', artists=artists)


@app.route('/getArtists.json')
def get_artists():
    iDisplayStart = int(request.args.get('iDisplayStart', '0'))
    iDisplayLength = int(request.args.get('iDisplayLength', '100'))
    sSearch = request.args.get('sSearch', '')
    iSortCol_0 = request.args.get('iSortCol_0', '')
    sSortDir_0 = request.args.get('sSortDir_0', 'asc')

    filtered = []
    totalcount = 0
    session = connect()

    sortcolumn = Artist.name
    if iSortCol_0 == '2':
        # Status column.
        sortcolumn = Artist.status
    elif iSortCol_0 == '3':
        # 'ReleaseDate'
        sortcolumn = Release.release_date
    elif iSortCol_0 == '4':
        sortbyhavepercent = True

    if sSearch == "":
        filtered = session.query(Artist).order_by(Artist.name.asc())
    else:
        filtered = session.query(Artist).filter_by(name=sSearch).order_by(Artist.name.asc())

    totalcount = filtered.count()

    artists = filtered[iDisplayStart:(iDisplayStart + iDisplayLength)]
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
        if latest_album:
            row['ReleaseDate'] = ""
            row['LatestAlbum'] = latest_album.name
            row['AlbumID'] = latest_album.id
            if artist['ReleaseDate'] > datetime.date.today():
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
