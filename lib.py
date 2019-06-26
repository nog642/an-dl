#!/usr/bin/env python3
from functools import wraps
import signal
import sys

STDOUT_UNBUFFERED = False
DEFAULT_ENCODING_SET = False


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


class Unbuffered:

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def unbuffer():
    global STDOUT_UNBUFFERED
    if not STDOUT_UNBUFFERED:
        sys.stdout = Unbuffered(sys.stdout)
        STDOUT_UNBUFFERED = True
