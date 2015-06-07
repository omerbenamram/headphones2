import logbook
from beets.autotag import tag_album, Recommendation
from headphones2.media.tagger import Tagger

logger = logbook.Logger(__name__)

class SimpleBeetsTagger(Tagger):

    modifies = []
    kind = 'MetadataProcessor'

    def __init__(self):
        super(SimpleBeetsTagger).__init__()

    # TODO: implement metadata editing
    @staticmethod
    def process(list_of_items, expected_artist=None, expected_album=None):
        artist_name, album_name, album_recommendation_list, recommendation = \
            tag_album(list_of_items, search_artist=expected_artist, search_album=expected_album)

        if recommendation is Recommendation.none:
            logger.debug('Failed matching album')
            return None
        else:
            return album_recommendation_list[0].album_id
