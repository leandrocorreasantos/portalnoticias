from http.client import NOT_FOUND, OK, CREATED, BAD_REQUEST

from flask import jsonify
from marshmallow import Schema, fields, validate


class DefaultSchema(Schema):

    @classmethod
    def build(self, data):
        return jsonify(cls().dump(data)), OK.value
    
    @classmethod
    def created(self, data):
        return jsonify(cls().dump(data)), CREATED.value


class CategoriaSchema(DefaultSchema):
    id = fields.Integer()
    nome = fields.String(validate=validate.Length(max=100))
    slug = fields.String(dump_only=True)


class NoticiaSchema(DefaultSchema):
    id = fields.Integer()
    titulo = fields.String()
    slug = fields.String(dump_only=True)
    conteudo = fields.String()
    publicado = fields.Boolean(default=False)
    data_publicacao = fields.DateTime()
    data_atualizacao = fields.DateTime()
    cliques = fields.Integer(default=0)
    meta_keywords = fields.String()
    meta_description = fields.String()


class UserSchema(DefaultSchema):
    id = fields.Integer()
    username = fields.String(validate=validate.Length(max=100, min=3))
    password = fields.String(
        load_only=True, 
        validate=validate.Length(min=6,max=255)
    )
    active = fields.Boolean(default=False)
    email = fields.String()
    email_confirmed_at = fields.DateTime()


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


class ValidationErrorSchema(Schema):
    message = fields.String(default="Validation Error")
    code = fields.Integer(default=400)
    description = fields.String(default="Error in data validation")

    @classmethod
    def build(self, messages):
        return jsonify(messages), BAD_REQUEST.value


class CategoriaValidationErrorSchema(ValidationErrorSchema):
    message = fields.String(default="Error on categoria validation")