import json
import unittest
from http.client import (
    BAD_REQUEST, CREATED, OK, METHOD_NOT_ALLOWED, UNAUTHORIZED
)
from api import db
from api.models import User, Role, UserRoles
from api.app import application
from api.config import TestingConfig
from werkzeug.security import generate_password_hash


class TestUsers(unittest.TestCase):

    def setUp(self):
        application.config.from_object(TestingConfig)
        self.app = application.test_client()
        db.create_all()
        admin = Role(**{"id": 1, "name": "admin"})
        jornalista = Role(**{"id":2, "name": "jornalista"})
        user = User()
        user.id = 1
        user.username = 'admin'
        user.password = generate_password_hash('123456')
        user.email = 'test@localhost'
        user.first_name = 'admin'
        user.last_name = 'test'
        userroles = UserRoles(**{"id": 1, "user_id": 1, "role_id": 1})
        db.session.add(admin)
        db.session.add(jornalista)
        user.roles.append(admin)
        db.session.add(user)
        db.session.commit()
        response = self.app.post(
            "/v1/user/login",
            json={'username': user.username, 'password': '123456'}
        )
        token = json.loads(response.data)
        self.token = "Bearer {}".format(token['access_token'])
        self.headers = {'Authorization': self.token}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_user_without_login_should_return_error(self):
        response = self.app.get('/v1/user')
        self.assertEqual(response.status_code, UNAUTHORIZED.value)

    def test_get_user_data_with_token_should_return_success(self):
        response = self.app.get('/v1/user', headers=self.headers)
        user = json.loads(response.data)['logged_in_as']
        self.assertEqual(response.status_code, OK.value)
        self.assertEqual(user, 'admin')

    def test_post_user_data_with_token_should_return_success(self):
        data = {
            "id": 2,
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
