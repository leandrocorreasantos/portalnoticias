# -*- coding: utf-8 -*-
from api import db
from slugify import slugify
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    active = db.Column(
        'is_active', db.Boolean(), nullable=False, server_default='1'
    )
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # email_confirmed_at = db.Column(db.DateTime())
    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'
    ))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'
    ))


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

    @property
    def slug(self):
        return slugify(self.nome)


class Noticia(db.Model):
    __tablename__ = 'noticias'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text)
    publicado = db.Column(db.Boolean(), server_default='0')
    data_publicacao = db.Column(db.DateTime(), default=datetime.now())
    data_atualizacao = db.Column(db.DateTime(), default=datetime.now())
    cliques = db.Column(db.Integer(), server_default='0')
    meta_keywords = db.Column(db.String(100))
    meta_description = db.Column(db.String(255))
