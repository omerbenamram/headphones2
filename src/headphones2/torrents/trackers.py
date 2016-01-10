from torrentsearcher import KickAssTorrentsSearcher, PirateBaySearcher


def get_configured_tracker_searchers():
    return [
        KickAssTorrentsSearcher(),
        PirateBaySearcher()
    ]
