import requests

TIMEOUT = 60.0 # seconds
REQUEST_LIMIT = 1.0 / 5 # seconds
ENTRY_POINT = "http://ws.audioscrobbler.com/2.0/"
API_KEY = "395e6ec6bb557382fc41fde867bce66f"


def lastfm_api_wrapper(method, **kwargs):
    kwargs["method"] = method
    kwargs.setdefault("api_key", API_KEY)
    kwargs.setdefault("format", "json")

    return requests.get(ENTRY_POINT, timeout=TIMEOUT, params=kwargs).json()