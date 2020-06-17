import json
import unittest
from http.client import (
    CREATED, OK, UNAUTHORIZED, NOT_FOUND
)
from api import db, log
from api.models import User, Role
from api.app import application
from api.config import TestingConfig
from werkzeug.security import generate_password_hash


class TestUsers(unittest.TestCase):

    def setUp(self):
        application.config.from_object(TestingConfig)
        self.app = application.test_client()
        try:
            db.create_all()
        except Exception as e:
            print("Erro ao criar tabelas: {}".format(e))
        admin = Role(**{"id": 1, "name": "admin"})
        jornalista = Role(**{"id": 2, "name": "jornalista"})
        user = User(**{
            "id": 1,
            "username": "admin",
            "password": generate_password_hash("123456"),
            "email": "test@localhost",
            "first_name": "admin",
            "last_name": "test"
        })
        db.session.add(admin)
        db.session.add(jornalista)
        try:
            db.session.commit()
            db.session.flush()
        except Exception as e:
            log.info("users and groups already exists")

        user.roles.append(admin)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            log.info("user roles already exists")

        response = self.app.post(
            "/v1/user/login",
            json={"username": "admin", "password": "123456"}
        )
        token = json.loads(response.data)
        self.token = "Bearer {}".format(token['access_token'])
        self.headers = {'Authorization': self.token}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_user_without_login_should_return_error(self):
        response = self.app.get('/v1/user', headers=None)
        self.assertEqual(response.status_code, UNAUTHORIZED.value)

    def test_get_user_data_with_token_should_return_success(self):
        response = self.app.get('/v1/user', headers=self.headers)
        user = json.loads(response.data)['logged_in_as']
        self.assertEqual(response.status_code, OK.value)
        self.assertEqual(user, 'admin')

    def _test_post_user_data_with_token_should_return_success(self):
        # @FIXME verificar funcionamento
        data = {
            "username": "jornalista",
            "password": "123456",
            "email": "jornalista@jornal.com.br",
            "first_name": "jornalista",
            "last_name": "test",
            "role_ids": [2]
        }
        response = self.app.post('/v1/user', json=data, headers=self.headers)
        self.assertEqual(response.status_code, CREATED.value)

    def test_put_new_username_for_user_should_return_success(self):
        data = {
            "id": 1,
            "username": "manager",
            "email": "admin@localhost",
            "first_name": "admin",
            "last_name": "test",
            "role_ids": [1]
        }
        response = self.app.put('/v1/user/1', json=data, headers=self.headers)
        self.assertEqual(response.status_code, OK.value)

    def test_delete_user_should_return_success(self):
        response = self.app.delete('/v1/user/1', headers=self.headers)
        self.assertEqual(response.status_code, OK.value)

    def test_login_user_should_return_token(self):
        login_data = {"username": "admin", "password": "123456"}
        response = self.app.post('/v1/user/login', json=login_data)
        token = json.loads(response.data)
        assert 'access_token' in token

    def test_login_with_not_username_valid_should_return_not_found_error(self):
        login_data = {"username": "non_existent", "password": "123456"}
        response = self.app.post('/v1/user/login', json=login_data)
        self.assertEqual(response.status_code, NOT_FOUND.value)
