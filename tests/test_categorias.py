from tests import create_user_and_get_headers
from http.client import (
    BAD_REQUEST, CREATED, OK, METHOD_NOT_ALLOWED, UNAUTHORIZED
)
from api.app import application
from api.config import TestingConfig
application.config.from_object(TestingConfig)
app = application.test_client()

headers = create_user_and_get_headers()


def test_post_without_data_should_return_validation():
    response = app.post('/v1/categoria', json={}, headers=headers)
    assert response.status_code == BAD_REQUEST.value


def test_post_with_no_data_should_return_bad_request():
    response = app.post('/v1/categoria', json=None, headers=headers)
    assert response.status_code == BAD_REQUEST.value


def test_post_new_categoria_should_return_created_code():
    categoria = {"id": 1, "nome": "created"}
    response = app.post('/v1/categoria', json=categoria, headers=headers)
    assert response.status_code == CREATED.value


def test_put_categoria_without_data_should_return_bad_request():
    response = app.put('/v1/categoria/1', json={}, headers=headers)
    assert response.status_code == BAD_REQUEST.value


def test_put_categoria_update_should_return_ok_value():
    update = {"id": 1, "nome": "edited"}
    response = app.put('/v1/categoria/1', json=update, headers=headers)
    assert response.status_code == OK.value


def test_delete_categoria_without_id_should_return_not_allowed():
    response = app.delete('/v1/categoria', headers=headers)
    assert response.status_code == METHOD_NOT_ALLOWED.value


def test_delete_categoria_should_return_ok():
    response = app.delete("/v1/categoria/1", headers=headers)
    assert response.status_code == OK.value
# @TODO: test all protected endpoints with no headers if return unauthorized


def test_post_categoria_with_no_data_should_return_bad_request():
    response = app.post('/v1/categoria', json={}, headers=headers)
    assert response.status_code == BAD_REQUEST.value


def test_put_categoria_with_no_data_should_return_bad_request():
    response = app.put('/v1/categoria/1', json={}, headers=headers)
    assert response.status_code == BAD_REQUEST.value


def test_put_categoria_with_no_id_should_return_not_allowed():
    response = app.put('/v1/categoria', json={}, headers=headers)
    assert response.status_code == METHOD_NOT_ALLOWED.value


def test_get_categoria_should_return_ok():
    response = app.get('/v1/categoria')
    assert response.status_code == OK.value


def test_post_data_without_header_should_return_unauthorized():
    categoria = {"id": 3, "nome": "foo"}
    response = app.post('/v1/categoria', json=categoria)
    assert response.status_code == UNAUTHORIZED.value


def test_put_data_without_header_should_return_unauthorized():
    categoria = {"id": 3, "nome": "foo"}
    response = app.put('/v1/categoria/3', json=categoria)
    assert response.status_code == UNAUTHORIZED.value


def test_delete_categoria_without_header_should_return_unauthorized():
    response = app.delete('/v1/categoria/1')
    assert response.status_code == UNAUTHORIZED.value
