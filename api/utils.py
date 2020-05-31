from functools import wraps
from http.client import UNAUTHORIZED
from flask_jwt_extended import (
    get_jwt_claims,
    verify_jwt_in_request
)
from flask import jsonify
from api import app


def restrict_access(levels):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            with app.app_context():
                try:
                    verify_jwt_in_request()
                except Exception as e:
                    return jsonify(
                        {'message': 'access denied'}
                    ), UNAUTHORIZED.value

                user_data = get_jwt_claims()
                if '*' in levels:
                    return function(*args, **kwargs)

                for role in user_data['roles']:
                    if role in levels:
                        return function(*args, **kwargs)

                return jsonify(
                    {'message': 'access denied'}
                ), UNAUTHORIZED.value

        return wrapper
    return decorator
