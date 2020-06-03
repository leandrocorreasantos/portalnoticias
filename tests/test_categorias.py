import json
import unittest
from unittest import mock
from http.client import BAD_REQUEST, CREATED
from api import db
from api.app import application
from api.config import TestingConfig

class TestCategorias(unittest.TestCase):

    def setUp(self):
        application.config.from_object(TestingConfig)
        self.app = application.test_client()
        db.create_all()
        db.session.commit()
        self.categoria = {"id": 1, "nome": "geral"}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_without_data_should_return_validation_error(self):
        response = self.app.post('/v1/categoria', json={})
        self.assertEqual(response.status_code, BAD_REQUEST.value)

    def test_post_with_no_data_should_return_bad_request_error(self):
        response = self.app.post('/v1/categoria', json=None)
        self.assertEqual(response.status_code, BAD_REQUEST.value)

    @mock.patch('api.db')
    def test_post_new_category_should_return_created_code(self, db_mock):
        db_mock.query.all.return_value = [{"id": 1, "nome": "geral"}]
        response = self.app.post('/v1/categoria', json=self.categoria)
        self.assertEqual(response.status_code, CREATED.value)
