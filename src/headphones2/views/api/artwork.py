import flask
import logbook
import requests
from flask.ext.restful import Resource, reqparse, abort

from headphones2.external.lastfm import lastfm_api_wrapper
from headphones2.tasks import get_artwork_for_album_task

logger = logbook.Logger()

parser = reqparse.RequestParser()
parser.add_argument('fetch_image')
parser.add_argument('type')
parser.add_argument('size')
parser.add_argument('id')


class Artwork(Resource):
    def get(self):
        args = parser.parse_args()
        image_type = args.get('type')
        if not image_type:
            abort(500)

        mbid, size, should_fetch_image = args.get('id'), args.get('size'), args.get('fetch_image')
        if image_type == 'artist':
            return self.get_artist_artwork(mbid=mbid, size=size, fetch_image=should_fetch_image)
        elif image_type == 'album':
            return self.get_album_cover_art(rgid=mbid, size=size, fetch_image=should_fetch_image)

    @staticmethod
    def get_album_cover_art(rgid, size='small', fetch_image=False):
        """
        :param rgid: musicbrainz releasegroup_id
        :param size: large (500px) or small (250px)
        :return: binary jpeg
        """
        urls = get_artwork_for_album_task(rgid).get(True)
        if not urls:
            abort(404)

        chosen = urls.get(size)
        if not fetch_image:
            return chosen

        img = requests.get(chosen)
        if not img.ok:
            abort(404)

        resp = flask.make_response(img.content)
        resp.content_type = "image/jpeg"
        return resp

    @staticmethod
    def get_artist_artwork(mbid, size='small', fetch_image=False):
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
        chosen = size_dict[size]
        if not chosen:
            logger.warning(('No image found for ({id}, {size}'.format(id=mbid, size=size)))
            abort(404)

        if not fetch_image:
            return size_dict[size]

        img = requests.get(size_dict[size])

        if not img.ok:
            abort(404)

        resp = flask.make_response(img.content)
        resp.content_type = "image/jpeg"
        return resp
