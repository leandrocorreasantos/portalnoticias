from http.client import (
    NOT_FOUND,
    OK,
    CREATED,
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR
)

from flask import jsonify
from marshmallow import Schema, fields, validate


class DefaultSchema(Schema):

    @classmethod
    def build(cls, data):
        return jsonify(cls().dump(data)), OK.value

    @classmethod
    def created(cls, data):
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
        # load_only=True,
        validate=validate.Length(min=6,max=255)
    )
    active = fields.Boolean(default=False)
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    roles = fields.List(fields.Nested('RoleSchema'))
    role_ids = fields.List(fields.Integer(), load_only=True)


class RoleSchema(DefaultSchema):
    id = fields.String()
    name = fields.String()

# ERROR MESSAGES

class InternalServerErrorSchema(Schema):
    message = fields.String(default="Internal Server Error")
    code = fields.Integer(default=INTERNAL_SERVER_ERROR)
    description = fields.String(default="Internal Server Error")

    @classmethod
    def build(cls, message=None):
        return jsonify(cls().dump(
            {"message": message}
        )), INTERNAL_SERVER_ERROR.value


class EmptyDataSchema(Schema):
    message = fields.String(default="Empty data")
    code = fields.Integer(default=BAD_REQUEST)
    description = fields.String(default="Request data is empty")

    @classmethod
    def build(cls):
        return jsonify(cls().dump({})), BAD_REQUEST.value


# NOT FOUND
class NotFoundSchema(Schema):
    message = fields.String(default="Not Found")
    code = fields.Integer(default=NOT_FOUND)
    description = fields.String(default="Data Not Found")

    @classmethod
    def build(cls):
        return jsonify(cls().dump({})), NOT_FOUND.value


class CategoriaNotFoundSchema(NotFoundSchema):
    message = fields.String(default="Categoria Not Found")


class NoticiaNotFoundSchema(NotFoundSchema):
    message = fields.String(default="Noticia Not Found")


class UserNotFoundSchema(NotFoundSchema):
    message = fields.String(default="User Not Found")


class RoleNotFoundSchema(NotFoundSchema):
    message = fields.String(default="Role Not Found")


# VALIDATION ERROR
class ValidationErrorSchema(Schema):

    @classmethod
    def build(cls, messages):
        return jsonify(messages), BAD_REQUEST.value


class CategoriaValidationErrorSchema(ValidationErrorSchema):
    message = fields.String(default="Categoria validation error")


class NoticiaValidationErrorSchema(ValidationErrorSchema):
    message = fields.String(default="Noticia validation error")


class UserValidationErrorSchema(ValidationErrorSchema):
    message = fields.String(default="User Validation Error")


class RoleValidationErrorSchema(ValidationErrorSchema):
    message = fields.String(default="Role Validation Error")
