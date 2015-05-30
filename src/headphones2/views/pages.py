import datetime
from flask import Blueprint, request
import logbook
from headphones2.utils import find_artist_by_name, find_releases
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
