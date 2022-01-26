import time

from .. import exceptions

def handle_soft_limit(response, msg=None, **kwargs):
    print("WARNING: soft limit reached. Pausing for a second.")
    time.sleep(1)
    return msg

def handle_hard_limit(response, msg=None, **kwargs):
    error_msg = "ERROR: hard limit for number of requests per minute reached."
    raise exceptions.TooManyRequests(error_msg)

def handle_blocked(response, msg=None, **kwargs):
    error_msg = "ERROR: you have been blocked. Possibly due to too many requests."
    raise exceptions.BlockedFromAPI(error_msg)

def handle_service_unavailable(response, msg=None, **kwargs):
    error_msg = "ERROR: Service unavailable. Possibly you are blocked due to too many requests."
    raise exceptions.ServiceUnavailable(error_msg)


DEFAULT_STATUS_HANDLERS = {
    # SOFT AND HARD RATE LIMIT HANDLERS
    435: handle_soft_limit,
    402: handle_hard_limit,
    429: handle_hard_limit,
    430: handle_blocked, 
    434: handle_blocked, 
    503: handle_service_unavailable,
}
