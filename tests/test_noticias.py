import pytest
from unittest import mock
from tests import create_user_and_get_headers
from http.client import (
    OK, UNAUTHORIZED, BAD_REQUEST, METHOD_NOT_ALLOWED, CREATED
)
from api import db
from api.app import application
from api.models import Noticia
from api.config import TestingConfig
application.config.from_object(TestingConfig)
app = application.test_client()


headers = create_user_and_get_headers()

noticia = {
    "categoria_id": 1,
    "titulo": "noticia test",
    "conteudo": "lorem ipsum dolor sit amet",
    "meta_keywords": "noticia, test",
    "meta_description": "noticia test lorem ipsum"
}

categoria = {"id": 1, "nome": "foo"}

def test_get_noticias_with_auth_user_should_return_success():
    response = app.get('/v1/noticia', headers=headers)
    assert response.status_code == OK.value

def test_get_noticias_with_guest_user_should_return_success():
    response = app.get('/v1/noticia')
    assert response.status_code == OK.value

def test_post_noticia_with_no_header_should_return_unauthorized():
    response = app.post('/v1/noticia', json=noticia)
    assert response.status_code == UNAUTHORIZED.value

def test_put_noticia_with_no_header_should_return_unauthorized():
    response = app.put('/v1/noticia/1', json=noticia)
    assert response.status_code == UNAUTHORIZED.value

def test_delete_noticia_with_no_header_should_return_unauthorized():
    response = app.delete('/v1/noticia/1')
    assert response.status_code == UNAUTHORIZED.value

# @TODO: test endpoints with no data if return error
def test_post_noticia_with_no_data_should_return_bad_request():
    response = app.post('/v1/noticia', json={}, headers=headers)
    assert response.status_code == BAD_REQUEST.value

def test_put_noticia_with_no_data_should_return_bad_request():
    response = app.put('/v1/noticia/1', json={}, headers=headers)
    assert response.status_code == BAD_REQUEST.value

def test_delete_noticia_without_id_should_return_not_allowed():
    response = app.delete('/v1/noticia', headers=headers)
    assert response.status_code == METHOD_NOT_ALLOWED.value
# @TODO: test endpoints with data if return ok

def test_post_noticia_should_return_created():
    response = app.post('/v1/noticia', json=noticia, headers=headers)
    assert response.status_code == CREATED.value

def test_put_noticia_should_return_ok():
    response = app.post('/v1/categoria', json=categoria, headers=headers)
    assert response.status_code == CREATED.value
    noticia['id'] = 1
    noticia['titulo'] = 'noticia updated'
    response = app.put('/v1/noticia/1', json=noticia, headers=headers)
    assert response.status_code == OK.value

def test_delete_noticia_should_return_ok():
    response = app.delete('/v1/noticia/1', headers=headers)
    assert response.status_code == OK.value
