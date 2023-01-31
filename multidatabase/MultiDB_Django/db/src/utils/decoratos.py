import functools
import time

from db.src.utils.exceptions import ManagerDoesNotExist


class RetryError(Exception):
    """Exception \"of ending try counter\""""


def retry_request(counter=5, wait_time=0.25):
    def retry_request_wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            wr_counter, wait = counter, wait_time
            while wr_counter:
                try:
                    return func(*args, **kwargs)
                except ManagerDoesNotExist:
                    raise ManagerDoesNotExist
                except Exception:
                    if wr_counter:
                        time.sleep(wait)
                    else:
                        raise RetryError
                wr_counter -= 1
        return inner
    return retry_request_wrapper