# -*- coding: utf-8 -*-
from api import db
from slugify import slugify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class User(db.Model, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    active = db.Column(
        'is_active', db.Boolean(), nullable=False, server_default='1'
    )
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    # Define the relationship to Role via UserRoles
    roles = db.relationship(
        'Role', secondary='user_roles',
        backref='roles', lazy=True
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model, BaseModel):
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model, BaseModel):
    __tablename__ = 'user_roles'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'
    ))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'
    ))


class Categoria(db.Model, BaseModel):
    __tablename__ = 'categorias'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

    @property
    def slug(self):
        return slugify(self.nome)


class Noticia(db.Model, BaseModel):
    __tablename__ = 'noticias'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    categoria_id = db.Column(
        db.BigInteger(),
        db.ForeignKey('categorias.id', ondelete='SET NULL')
    )
    categoria = db.relationship('Categoria', backref='categoria', lazy=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text)
    publicado = db.Column(db.Boolean(), server_default='0')
    data_publicacao = db.Column(db.DateTime(), default=datetime.now())
    data_atualizacao = db.Column(db.DateTime(), default=datetime.now())
    cliques = db.Column(db.Integer(), server_default='0')
    meta_keywords = db.Column(db.String(100))
    meta_description = db.Column(db.String(255))
