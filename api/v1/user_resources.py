from http.client import OK
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    get_jwt_claims
)
from api import log, db, jwt
from api.v1.schema import (
    InternalServerErrorSchema,
    EmptyDataSchema,
    UserSchema, RoleSchema,
    UserValidationErrorSchema,
    UserNotFoundSchema,
)
from api.models import User, Role, UserRoles


@jwt.user_claims_loader
def add_claims_to_access_token(username):
    ''' save the user role on jwt token '''
    user = User.query.filter(
        User.username==username
    ).first()
    roles = []
    for role in user.roles:
        roles.append(role.name)
    return {'roles': roles}


class LoginView(MethodView):
    def post(self):
        # faz login e gera o token jwt
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        username = data.get('username')
        password = data.get('password')
        if not username and not password:
            return EmptyDataSchema().build()

        user = User.query.filter(
            User.username==username
        ).first()

        if not check_password_hash(user.password, password):
            return jsonify({'error': 'User or password are incorrect'}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200


class UserView(MethodView):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(
            logged_in_as=current_user,
            roles=get_jwt_claims()['roles']
        ), 200
        # dados do usuario (protegido) usa o jwt_token para pegar o username

    @jwt_required
    def post(self):
        data = request.get_json()

        if not data:
            return EmptyDataSchema().build()

        try:
            new_user = UserSchema().load(data)
        except ValidationError as err:
            return UserValidationErrorSchema().build(err.message)

        role_ids = new_user['role_ids']

        new_user['password'] = generate_password_hash(new_user['password'])

        user = User(**UserSchema().dump(new_user))

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
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
            print(e)
            db.session.rollback()
            return InternalServerErrorSchema().build("database Error")

        return UserSchema().build(
            UserSchema(exclude=('password',)).dump(user)
        )


    @jwt_required
    def put(self, user_id):
        user_id = int(user_id)
        new_user = None
        data = request.get_json()

        if not data or user_id is None:
            return EmptyDataSchema().build()

        user = User.query.filter(User.id==user_id).first()

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
            return InternalServerErrorSchema().build("Database error")

        return UserSchema().build(
            UserSchema(exclude=('password',)).dump(user)
        )

    @jwt_required
    def delete(self, user_id):
        user_id = int(user_id)

        user = User.query.get(user_id)
        if not user:
            return UserNotFoundSchema().build()

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return InternalServerErrorSchema().build("Database Error")

        return jsonify({}), OK.value
