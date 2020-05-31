from http.client import OK
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from api import log, db
from api.v1.schema import (
    InternalServerErrorSchema,
    CategoriaSchema, NoticiaSchema,
    CategoriaValidationErrorSchema,
    CategoriaNotFoundSchema,
    NoticiaValidationErrorSchema,
    EmptyDataSchema,
)
from api.models import Categoria, Noticia


class CategoriasView(MethodView):
    def get(self):
        categorias = Categoria.query.all()
        if not categorias:
            return jsonify({}), OK.value

        return jsonify(CategoriaSchema(many=True).dump(categorias)), OK.value

    def post(self):
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        try:
            categoria = CategoriaSchema().load(data)
        except ValidationError as err:
            return CategoriaValidationErrorSchema().build(err.messages)

        try:
            db.session.add(Categoria(**categoria))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during add categoria: {}".format(e))
            return InternalServerErrorSchema().build("Database Error")

        return CategoriaSchema().build(categoria)

    def put(self, categoria_id):
        data = request.get_json()
        if not data or categoria_id is None:
            return EmptyDataSchema().build()

        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return CategoriaNotFoundSchema().build()

        try:
            new_categoria = CategoriaSchema().load(data)
        except ValidationError as err:
            return CategoriaValidationErrorSchema().build(err.message)

        categoria.update(**new_categoria)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update categoria: {}".format(e))
            return InternalServerErrorSchema().build()

        return CategoriaSchema().dump(categoria)

    def delete(self, categoria_id):
        categoria_id = int(categoria_id)

        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return CategoriaNotFoundSchema().build()

        try:
            db.session.delete(categoria)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during delete categoria: {}".format(e))
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value


class NoticiasView(MethodView):
    def get(self):
        noticias = Noticia.query.all()
        return jsonify(NoticiaSchema(many=True).dump(noticias)), OK.value

    def post(self):
        data = request.get_json()
        try:
            noticia = NoticiaSchema.load(data)
        except ValidationError:
            return NoticiaValidationErrorSchema().build()

        try:
            db.session.add(noticia)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Errr during add noticia: {}".format(e))

        return NoticiaSchema().build(noticia)
