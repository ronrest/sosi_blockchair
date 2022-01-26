import requests

from sosi_api.exceptions import TooManyRequests

class BlockedFromAPI(requests.HTTPError):
    pass

class ServiceUnavailable(requests.HTTPError):
    pass
