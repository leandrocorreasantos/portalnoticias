from http.client import OK
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from api import log, db
from api.v1.schema import (
    InternalServerErrorSchema,
    EmptyDataSchema,
    UserSchema, RoleSchema,
    UserValidationErrorSchema,
    RoleValidationSchema,
    UserNotFoundSchema,
    RoleNotFoundSchema
)
from api.models import User, Role, UserRoles



class LoginView(MethodView):
    def post(self):

        # faz login e gera o token jwt


class RegisterView(MethodView):
    def post(self):
        pass
        # registra novo usuario


class UserView(MethodView):
    @jwt_required
    def get(self, user_id):
        pass
        # dados do usuario (protegido)
