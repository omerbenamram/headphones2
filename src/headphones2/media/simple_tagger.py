from beets.autotag import tag_album, Recommendation
from headphones2.media.tagger import Tagger


class SimpleBeetsTagger(Tagger):
    def __init__(self, task, expected_artist=None, expected_album=None):
        super(SimpleBeetsTagger).__init__(task)
        self._expected_artist = expected_artist
        self._expected_album = expected_album
        self._results = []

    @property
    def results(self):
        if not self._results:
            self.tag()
        return self._results

    def process(self):
        artist_name, album_name, album_recommendation_list, recommendation = \
            tag_album(self._task.items, search_artist=self._expected_artist, search_album=self._expected_album)

        if recommendation is not Recommendation.none:
            self._results.append(album_recommendation_list[0].album_id)
