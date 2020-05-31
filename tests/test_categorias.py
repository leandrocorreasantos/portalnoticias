# import json
import unittest
from api.app import application


class TestCategorias(unittest.TestCase):

    def setUp(self):
        self.app = application.test_client()
        self.categoria = {"name": "geral"}

    def test_post_without_data_should_return_validation_error(self):
        response = self.app.post('/v1/categoria', data={})
        print(response)

        self.assertEqual(response.status_code, 400)
