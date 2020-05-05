from http.client import NOT_FOUND

from flask import jsonify
from marshmallow import Schema, fields


class CategoriaSchema(Schema):
    id = fields.Integer()
    nome = fields.String()
    slug = fields.String()


class NoticiaSchema(Schema):
    id = fields.Integer()
    titulo = fields.String()
    conteudo = fields.String()
    publicado = fields.Boolean(default=False)
    data_publicacao = fields.DateTime()
    data_atualizacao = fields.DateTime()
    cliques = fields.Integer(default=0)
    meta_keywords = fields.String()
    meta_description = fields.String()


class NotFoundSchema(Schema):
    message = fields.String(default="Not Found")
    code = fields.Integer(default=404)
    description = fields.String(default="Data Not Found")

    @classmethod
    def build(cls):
        return jsonify(cls().dump({})), NOT_FOUND.value


class CategoriaNotFoundSchema(NotFoundSchema):
    message = fields.String(default="Categoria Not Found")


class NoticiaNotFoundSchema(NotFoundSchema):
    message = fields.String(default="Noticia Not Found")
