import string

import logbook

from .trackers import get_configured_tracker_searchers

logger = logbook.Logger(__name__)

from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english", ignore_stopwords=True)


def preprocess(name):
    name = name.lower().split('uploaded')[0]

    for w in ['kbps', 'bit'] + list('[](){}@.-'):
        name = name.replace(w, ' ')

    name = ' '.join([stemmer.stem(t) for t in word_tokenize(name)])

    return name


def get_search_term(release):
    artist = release.album.artist.name
    album = release.album.title
    release_year = release.release_date.year

    return

def verify_result(title, artist, term, lossless, ignored_words=None, required_words=None):
    title = re.sub('[\.\-\/\_]', ' ', title)

    # another attempt to weed out substrings. We don't want "Vol III" when we were looking for "Vol II"

    # Filter out remix search results (if we're not looking for it)
    if 'remix' not in term.lower() and 'remix' in title.lower():
        logger.info(
            "Removed %s from results because it's a remix album and we're not looking for a remix album right now.",
            title)
        return False

    # Filter out FLAC if we're not specifically looking for it
    if 'flac' in title.lower() and not lossless:
        logger.info(
            "Removed %s from results because it's a lossless album and we're not looking for a lossless album right now.",
            title)
        return False

    if ignored_words:
        for each_word in ignored_words:
            if each_word.lower() in title.lower():
                logger.info("Removed '%s' from results because it contains ignored word: '%s'", title, each_word)
                return False

    if required_words:
        for each_word in required_words:
            if each_word.lower() not in title.lower():
                logger.info("Removed '%s' from results because it doesn't contain required word: '%s'", title,
                            each_word)
                return False

    tokens = re.split('\W', term, re.IGNORECASE | re.UNICODE)

    for token in tokens:
        if not token:
            continue
        if token == 'Various' or token == 'Artists' or token == 'VA':
            continue
        if not re.search('(?:\W|^)+' + token + '(?:\W|$)+', title, re.IGNORECASE | re.UNICODE):
            cleantoken = ''.join(c for c in token if c not in string.punctuation)
            if not not re.search('(?:\W|^)+' + cleantoken + '(?:\W|$)+', title, re.IGNORECASE | re.UNICODE):
                dic = {'!': 'i', '$': 's'}
                dumbtoken = helpers.replace_all(token, dic)
                if not not re.search('(?:\W|^)+' + dumbtoken + '(?:\W|$)+', title, re.IGNORECASE | re.UNICODE):
                    logger.info("Removed from results: %s (missing tokens: %s and %s)", title, token, cleantoken)
                    return False

    return True


def searchTorrent(release, new=False, lossless_only=False, album_length=None, choose_specific_download=False):
    term, artistterm = get_search_term(release)

    logger.debug("Using search term: %s" % term)

    resultlist = []

    for searcher in get_configured_tracker_searchers():
        results = searcher.fetch_results(term)  # categories=Category.Music
        match = ''  # TODO: What is this?

        for result in results:
            resultlist.append((result.title, result.size, result.url, searcher, "torrent", match))


    # attempt to verify that this isn't a substring result
    # when looking for "Foo - Foo" we don't want "Foobar"
    # this should be less of an issue when it isn't a self-titled album so we'll only check vs artist
    # TODO: Lossless here is incorrect. It should be tree-way enum [Lossy, Lossless, Any]
    results = [result for result in resultlist if verify_result(result[0], artistterm, term, lossless_only)]

    # TODO: more_filtering ignore results based on the torrent size. Need to implement.
    # Additional filtering for size etc
    # if results and not choose_specific_download:
    # results = more_filtering(results, album, albumlength, new)

    return results
