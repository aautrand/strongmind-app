from functools import wraps

from flask import make_response


def common_response(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if type(result) is tuple:
            return make_response(result[0], result[1])

        return make_response(result)

    return wrapper
