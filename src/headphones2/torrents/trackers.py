from torrentsearcher import KickAssTorrentsSearcher, PirateBaySearcher, TorrentLeechSearcher


def get_configured_tracker_searchers():
    return [
        KickAssTorrentsSearcher(),
        PirateBaySearcher()
    ]
