from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logbook

logger = logbook.Logger(__name__)


# @api.route('/api/artwork/album/<string:rgid>/<string:size>')
# @cache.cached()
# def get_album_cover_art(rgid, size='small'):
#     """
#     :param rgid: musicbrainz releasegroup_id
#     :param size: large (500px) or small (250px)
#     :return: binary jpeg
#     """
#     urls = get_artwork_for_album_task(rgid).get(True)
#     if not urls:
#         abort(404)
#
#     chosen = urls.get(size)
#     img = requests.get(chosen)
#     if not img.ok:
#         abort(404)
#
#     resp = flask.make_response(img.content)
#     resp.content_type = "image/jpeg"
#     return resp
#
#
# @api.route('/api/artwork/artist/<string:mbid>/<string:size>')
# @cache.cached()
# def get_artist_artwork(mbid, size='small'):
#     """
#     :param mbid: musicbrainz artist_id
#     :param size: large (500px) or small (250px)
#     :return: binary jpeg
#     """
#     artist_info = lastfm_api_wrapper("artist.getinfo", mbid=mbid)
#     if not artist_info:
#         abort(404)
#
#     artist_artwork = artist_info['artist']['image']
#     # convert response list of dicts to something more usable
#     size_dict = {d['size']: d['#text'] for d in artist_artwork}
#     chosen = size_dict[size]
#     if not chosen:
#         logger.warning(('No image found for ({id}, {size}'.format(id=mbid, size=size)))
#         abort(404)
#
#     img = requests.get(size_dict[size])
#
#     if not img.ok:
#         abort(404)
#
#     resp = flask.make_response(img.content)
#     resp.content_type = "image/jpeg"
#     return resp
#
#
# @api.route('/markAlbums')
# def mark_albums():
#     request_args = dict(request.args)
#     action = request_args.pop('action')[0]
#     artist_id = request_args.pop('ArtistID')[0]
#
#     if action == 'WantedNew' or action == 'WantedLossless':
#         action = 'Wanted'
#
#     session = connect()
#
#     for album_id, on_or_off in request_args.items():
#         album = session.query(Album).filter_by(musicbrainz_id=album_id).one()
#         if on_or_off == ['on']:
#             logger.info('Marking {} as {}'.format(album, action))
#             album.status = Status.from_name(action)
#
#     session.commit()
#
#     # TODO: call 'search'
#
#     return ''
#
#
# @api.route('/api/album')
# def get_album():
#     album_id = request.args['AlbumID']
#     session = connect()
#     album = session.query(Album).filter_by(musicbrainz_id=album_id).first()
#     album_json = json.dumps({
#         'AlbumTitle': album.title,
#         'ArtistName': album.artist.name,
#         'Status': album.status.name
#     })
#     return album_json