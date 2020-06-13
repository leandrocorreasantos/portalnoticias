import functools
from http.client import UNAUTHORIZED
from flask import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request


def restrict_access(levels):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            roles = get_jwt_claims()['roles']
            authorized = False
            for role in roles:
                if role in levels:
                    authorized = True

            if authorized is False:
                return jsonify(msg='Access unauthorized'), UNAUTHORIZED.value

            return f(*args, **kwargs)

        return wrapper

    return decorator
