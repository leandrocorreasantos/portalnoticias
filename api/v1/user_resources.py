from http.client import (
    OK, UNAUTHORIZED, CREATED
)
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
        data = request.get_json()
        if not data:
            log.error('no data')
            return EmptyDataSchema().build()

        username = data.get('username')
        password = data.get('password')
        if not username and not password:
            log.error('no username or password')
            return EmptyDataSchema().build()

        user = User.query.filter(
            User.username == username
        ).first()

        if not check_password_hash(user.password, password):
            log.error('diff password')
            return jsonify(
                {'error': 'User or password are incorrect'}
            ), UNAUTHORIZED.value

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), OK.value

        # faz login e gera o token jwt


    @jwt_required
    @restrict_access(['admin', 'editor', 'jornalista'])
    def post(self):
        pass
        # registra novo usuario

        if not data:
            return EmptyDataSchema().build()

        try:
            new_user = UserSchema().load(data)
        except ValidationError as err:
            log.error(err)
            return UserValidationErrorSchema().build(err)

        role_ids = new_user['role_ids']

        new_user['password'] = generate_password_hash(new_user['password'])

        user = User(**UserSchema().dump(new_user))

        try:
            db.session.add(user)
            db.session.commit()
            db.session.flush()
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return InternalServerErrorSchema().build("Database Error")

        if role_ids:
            user.roles = []
            for role_id in role_ids:
                role = Role.query.get(role_id)
                user.roles.append(role)

        try:
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return InternalServerErrorSchema().build("database Error")

        return UserSchema().created(
            UserSchema(exclude=('password',)).dump(user)
        )

    @jwt_required
    @restrict_access(['admin' ,'editor', 'jornalista'])
    def put(self, user_id):
        user_id = int(user_id)
        new_user = None
        data = request.get_json()

        if not data or user_id is None:
            return EmptyDataSchema().build()
        user = User.query.get(user_id)

        if not user:
            return UserNotFoundSchema().build()

        try:
            new_user = UserSchema().load(data)
        except ValidationError as err:
            return UserValidationErrorSchema().build(err.message)

        role_ids = new_user.get('role_ids', None)

        new_user['password'] = user.password
        if 'new_password' in new_user:
            new_user['password'] = generate_password_hash(
                new_user['new_password']
            )

        user.update(**new_user)

        if role_ids:
            user.roles = []
            for role_id in role_ids:
                role = Role.query.get(role_id)
                user.roles.append(role)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update user: {}".format(e))
            return InternalServerErrorSchema().build("Database error")

        return UserSchema().build(
            UserSchema(exclude=('password',)).dump(user)
        )


class UserView(MethodView):
    @jwt_required
    @restrict_access(['admin'])
    def delete(self, user_id):
        user_id = int(user_id)

        user = User.query.get(user_id)
        if not user:
            return UserNotFoundSchema().build()

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Database Error: {}".format(e))
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value
