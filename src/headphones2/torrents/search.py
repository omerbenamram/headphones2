import re
import string
import logbook
from headphones2 import helpers
from .trackers import get_configured_tracker_searchers

logger = logbook.Logger(__name__)

# NOT WORKING
def get_search_term(release):
    album = release.album
    albumid = release.album.musicbrainz_id
    reldate = release.release_date
    year = reldate.year
    # MERGE THIS WITH THE TERM CLEANUP FROM searchNZB
    dic = {'...': '', ' & ': ' ', ' = ': ' ', '?': '', '$': 's', ' + ': ' ', '"': '', ',': ' ', '*': ''}
    semi_cleanalbum = helpers.replace_all(album['AlbumTitle'], dic)
    cleanalbum = helpers.latinToAscii(semi_cleanalbum)
    semi_cleanartist = helpers.replace_all(album['ArtistName'], dic)
    cleanartist = helpers.latinToAscii(semi_cleanartist)
    # Use provided term if available, otherwise build our own (this code needs to be cleaned up since a lot
    # of these torrent providers are just using cleanartist/cleanalbum terms
    if album['SearchTerm']:
        term = album['SearchTerm']

    else:
        # FLAC usually doesn't have a year for some reason so I'll leave it out
        # Various Artist albums might be listed as VA, so I'll leave that out too
        # Only use the year if the term could return a bunch of different albums, i.e. self-titled albums
        if album['ArtistName'] in album['AlbumTitle'] or len(album['ArtistName']) < 4 or len(album['AlbumTitle']) < 4:
            term = cleanartist + ' ' + cleanalbum + ' ' + year
        elif album['ArtistName'] == 'Various Artists':
            term = cleanalbum + ' ' + year
        else:
            term = cleanartist + ' ' + cleanalbum

    # Save user search term
    if album['SearchTerm']:
        usersearchterm = term
    else:
        usersearchterm = ''
    semi_clean_artist_term = re.sub('[\.\-\/]', ' ', semi_cleanartist).encode('utf-8', 'replace')
    semi_clean_album_term = re.sub('[\.\-\/]', ' ', semi_cleanalbum).encode('utf-8', 'replace')
    # Replace bad characters in the term and unicode it
    term = re.sub('[\.\-\/]', ' ', term).encode('utf-8')
    artistterm = re.sub('[\.\-\/]', ' ', cleanartist).encode('utf-8', 'replace')
    albumterm = re.sub('[\.\-\/]', ' ', cleanalbum).encode('utf-8', 'replace')
    return term, artistterm


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
        results = searcher.query_tracker(term)  # categories=Category.Music
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