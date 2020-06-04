import json
import unittest
from unittest import mock
from http.client import (
    BAD_REQUEST, CREATED, OK, METHOD_NOT_ALLOWED
)
from api import db
from api.models import Categoria
from api.app import application
from api.config import TestingConfig

class TestCategorias(unittest.TestCase):

    def setUp(self):
        application.config.from_object(TestingConfig)
        self.app = application.test_client()
        db.create_all()
        categoria = {"id": 1, "nome": "created"}
        db.session.add(Categoria(**categoria))
        db.session.commit()
        self.categoria = {"id": 2, "nome": "geral"}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_without_data_should_return_validation_error(self):
        response = self.app.post('/v1/categoria', json={})
        self.assertEqual(response.status_code, BAD_REQUEST.value)

    def test_post_with_no_data_should_return_bad_request_error(self):
        response = self.app.post('/v1/categoria', json=None)
        self.assertEqual(response.status_code, BAD_REQUEST.value)

    def test_post_new_categoria_should_return_created_code(self):
        response = self.app.post('/v1/categoria', json=self.categoria)
        self.assertEqual(response.status_code, CREATED.value)

    def test_put_categoria_without_data_should_return_bad_request(self):
        response = self.app.put('/v1/categoria/1', json={})
        self.assertEqual(response.status_code, BAD_REQUEST.value)

    def test_put_categoria_update_should_return_ok_value(self):
        update = {"id": 1, "nome": "edited"}
        response = self.app.put('/v1/categoria/1', json=update)
        self.assertEqual(response.status_code, OK.value)

    def test_delete_categoria_without_id_should_return_method_not_allowed(self):
        response = self.app.delete('/v1/categoria')
        self.assertEqual(response.status_code, METHOD_NOT_ALLOWED.value)

    def test_delete_categoria_should_return_ok(self):
        response = self.app.delete("/v1/categoria/1")
        self.assertEqual(response.status_code, OK.value)
