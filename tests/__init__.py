import pytest
import json
from api import db, log
from api.models import User, Role, Categoria
from api.app import application
from api.config import TestingConfig
from werkzeug.security import generate_password_hash


@pytest.fixture
def create_user_and_get_headers():
    application.config.from_object(TestingConfig)
    app = application.test_client()

    try:
        db.session.remove()
        db.drop_all()
        db.create_all()
    except Exception as e:
        print("Erro ao criar tabelas: {}".format(e))

    # categoria = Categoria(**{"id": 1, "nome": "foo"})
    # try:
    #     db.session.add(categoria)
    #     db.session.commit()
    # except Exception as e:
    #     db.session.rollback()

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
        db.session.rollback()
        log.info("users and groups already exists")

    user.roles.append(admin)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log.info("user roles already exists")

    response = app.post(
        "/v1/user/login",
        json={"username": "admin", "password": "123456"}
    )
    user_token = json.loads(response.data)
    token = "Bearer {}".format(user_token['access_token'])
    headers = {'Authorization': token}
    return headers


@pytest.fixture
def create_categoria_from_noticia():
    categoria = Categoria(**{"id": 1, "nome": "foo"})
    try:
        db.session.add(categoria)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
