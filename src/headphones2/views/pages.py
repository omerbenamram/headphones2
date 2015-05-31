import datetime
from flask import Blueprint, request, redirect, url_for
import logbook
from .. import config
from ..importer import add_artist_to_db
from ..orm.serialize import artist_to_dict
from ..utils import find_artist_by_name, find_releases
from .templates import serve_template
from ..orm import *

logger = logbook.Logger(__name__)

pages = Blueprint('pages', __name__)


@pages.route('/')
@pages.route('/home')
def home():
    return serve_template('index.html', title='Home')


@pages.route('/upcoming')
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


@pages.route('/manage')
def manage():
    session = connect()
    empty_artists = session.query(Artist).filter(~Artist.albums.any())
    return serve_template(templatename="manage.html", title="Manage", emptyArtists=empty_artists)


@pages.route('/history')
def history():
    session = connect()
    history = []  # session.query(Snached).filter(~Snached.status.ilike('Seed%')).order_by(Snached.date_added.desc())
    return serve_template(templatename="history.html", title="History", history=history)


@pages.route('/logs')
def logs():
    return serve_template(templatename="logs.html", title="Log")


@pages.route('/manageArtists')
def manage_artists():
    session = connect()
    artists = session.query(Artist).order_by(Artist.name)
    return serve_template(templatename="manageartists.html", title="Manage Artists", artists=artists)


@pages.route('/search')
def search():
    name = request.args['name']
    type = request.args['type']

    if type == 'artist':
        results = find_artist_by_name(name, limit=10)

        formatted_results = []

        for result in results:
            formatted_results.append({
                'score': result['ext:score'],
                'id': result['id'],
                'uniquename': result['name'],
            })
    else:
        assert False
        results = find_releases(name, limit=10)

        formatted_results = []

        for result in results:
            formatted_results.append({
                'score': result['ext:score'],
                'id': result['id'],
                'title': result['title'],
            })

    return serve_template(templatename="searchresults.html", title='Search Results "{name}"'.format(name=name),
                          searchresults=formatted_results, name=name, type=type)


@pages.route('/addArtist')
def add_artist():
    artist_id = request.args['artistid']
    # session = connect()
    # add_artist_to_db(artist_id, session)

    return redirect('/artistPage&ArtistID=' + artist_id)


@pages.route('/artistPage')
def artist_page():
    artist_id = request.args['ArtistID']
    session = connect()
    artist = session.query(Artist).filter_by(musicbrainz_id=artist_id).one()

    # Serve the extras up as a dict to make things easier for new templates (append new extras to the end)
    # extras_list = headphones.POSSIBLE_EXTRAS
    # if artist['Extras']:
    # artist_extras = map(int, artist['Extras'].split(','))
    # else:
    # artist_extras = []
    #
    # extras_dict = OrderedDict()
    #
    # i = 1
    # for extra in extras_list:
    #     if i in artist_extras:
    #         extras_dict[extra] = "checked"
    #     else:
    #         extras_dict[extra] = ""
    #     i += 1
    formatted_artist = artist_to_dict(artist)
    formatted_artist['IncludeExtras'] = False

    formatted_albums = []

    for album in artist.albums:
        formatted_album = album_to_dict(album)

        if formatted_album['Status'] == 'Skipped':
            grade = 'Z'
        elif formatted_album['Status'] == 'Wanted':
            grade = 'X'
        elif formatted_album['Status'] == 'Snatched':
            grade = 'C'
        elif formatted_album['Status'] == 'Ignored':
            grade = 'I'
        else:
            grade = 'A'
        formatted_album['Grade'] = grade

        release = album.releases[0]
        totaltracks = release.tracks.count()
        havetracks = release.tracks.filter((Track.location != None) | (Track.matched == "failed")).count()

        try:
            percent = (havetracks * 100.0) / totaltracks
            if percent > 100:
                percent = 100
        except (ZeroDivisionError, TypeError):
            percent = 0
            totaltracks = '?'
        formatted_album['Percent'] = percent
        formatted_album['HaveTracks'] = havetracks
        formatted_album['TotalTracks'] = totaltracks

        # avgbitrate = myDB.action("SELECT AVG(BitRate) FROM tracks WHERE AlbumID=?", [album['AlbumID']]).fetchone()[0]
        # if avgbitrate:
        #     bitrate = str(int(avgbitrate)/1000) + ' kbps'
        # else:
        #     bitrate = ''
        formatted_album['Bitrate'] = ''

        album_formats = [track.format for track in release.tracks]
        if len(album_formats) == 1:
            album_format = album_formats[0]
        elif len(album_formats) > 1:
            album_format = 'Mixed'
        else:
            album_format = ''

        formatted_album['Format'] = album_format

        formatted_album['IsLossy'] = formatted_album['Format'] in config.LOSSY_MEDIA_FORMATS


    return serve_template(templatename="artist.html",
                          title=artist.name,
                          artist=formatted_artist,
                          albums=formatted_albums,
                          extras={})

