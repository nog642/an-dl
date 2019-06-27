#!/usr/bin/env python3
from functools import wraps
import signal


def timeout(seconds, error_message=None):
    """
    Decorator that will cause the function decorated to time out (raise a
    TimeoutError) after a given number of seconds. These cannot be nested.
    :param seconds:
    :param error_message:
    :return:
    """
    def decorator(func):
        if error_message is None:
            def handle_timeout(signum, frame):
                raise TimeoutError
        else:
            def handle_timeout(signum, frame):
                raise TimeoutError(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            old_handler = signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            return result

        return wrapper

    return decorator
