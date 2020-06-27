import json
import pytest
from tests import create_user_and_get_headers
from http.client import (
    NOT_FOUND, CREATED, BAD_REQUEST, UNAUTHORIZED, OK
)
from api.app import application
from api.config import TestingConfig
application.config.from_object(TestingConfig)
app = application.test_client()

headers = create_user_and_get_headers()


def test_login_with_not_username_valid_should_return_not_found_error():
    login_data = {"username": "non_existent", "password": "123456"}
    response = app.post('/v1/user/login', json=login_data, headers=headers)
    assert response.status_code == NOT_FOUND.value

def test_get_user_without_login_should_return_error():
    response = app.get('/v1/user', headers=None)
    assert response.status_code == UNAUTHORIZED.value

def test_get_user_data_with_token_should_return_success():
    response = app.get('/v1/user', headers=headers)
    user = json.loads(response.data)['logged_in_as']
    assert response.status_code == OK.value
    assert user == 'admin'

def test_post_user_data_with_token_should_return_success():
    data = {
        "id": 2,
        "username": "jornalista",
        "password": "123456",
        "email": "jornalista@jornal.com.br",
        "first_name": "jornalista",
        "last_name": "test",
        "role_ids": [2]
    }
    response = app.post('/v1/user', json=data, headers=headers)
    assert response.status_code == CREATED.value

def test_put_new_username_for_user_should_return_success():
    data = {
        "id": 1,
        "username": "manager",
        "email": "admin@localhost",
        "first_name": "admin",
        "last_name": "test",
        "role_ids": [1]
    }
    response = app.put('/v1/user/1', json=data, headers=headers)
    assert response.status_code == OK.value

def test_delete_user_should_return_success():
    response = app.delete('/v1/user/1', headers=headers)
    assert response.status_code == OK.value

def test_login_user_should_return_token():
    login_data = {"username": "jornalista", "password": "123456"}
    response = app.post('/v1/user/login', json=login_data)
    token = json.loads(response.data)
    assert 'access_token' in token

def test_login_with_not_username_valid_should_return_not_found_error():
    login_data = {"username": "non_existent", "password": "123456"}
    response = app.post('/v1/user/login', json=login_data)
    assert response.status_code == NOT_FOUND.value

