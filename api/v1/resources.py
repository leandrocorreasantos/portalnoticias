from sqlalchemy import and_
from datetime import datetime
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
    NoticiaNotFoundSchema,
    NoticiaValidationErrorSchema,
    EmptyDataSchema,
)
from api.models import Categoria, Noticia
from api.utils import restrict_access
from flask_jwt_extended import (
    jwt_required, jwt_optional, get_jwt_identity
)


class CategoriasView(MethodView):
    def get(self, categoria_id=None):
        page = request.args.get('page', 1, type=int)
        offset = request.args.get('offset', 10, type=int)

        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            return jsonify(CategoriaSchema().dump(categoria))

        categorias = Categoria.query.paginate(page, offset, False).items
        return jsonify(CategoriaSchema(many=True).dump(categorias)), OK.value

    @jwt_required
    @restrict_access(['admin', 'editor'])
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

        return CategoriaSchema().created(categoria)

    @jwt_required
    @restrict_access(['admin', 'editor'])
    def put(self, categoria_id):
        categoria_id = int(categoria_id)
        data = request.get_json()
        if not data or categoria_id == 0:
            return EmptyDataSchema().build()

        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            log.error('Categoria not found')
            return CategoriaNotFoundSchema().build()

        try:
            new_categoria = CategoriaSchema().load(data)
        except ValidationError as err:
            log.error('Error while validate Categoria: {}'.format(err))
            return CategoriaValidationErrorSchema().build(err.message)

        categoria.update(**new_categoria)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update categoria: {}".format(e))
            return InternalServerErrorSchema().build()

        return CategoriaSchema().dump(categoria)

    @jwt_required
    @restrict_access(['admin', 'editor'])
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
    @jwt_optional
    def get(self, noticia_id=None):
        filters = []
        noticias = []
        noticia = None
        pagination = {}
        page = request.args.get('page', 1, type=int)
        offset = request.args.get('offset', 10, type=int)

        current_user = get_jwt_identity()
        if current_user is None:
            filters.append(Noticia.publicado.is_(True))
            filters.append(Noticia.data_publicacao <= datetime.now())

        if noticia_id:
            filters.append(Noticia.id == noticia_id)
            noticia = Noticia.query.filter(and_(*filters)).first()
            return jsonify(NoticiaSchema().dump(noticia)), OK.value

        categoria_id = request.args.get('cat', None, type=int)

        if categoria_id:
            filters.append(Noticia.categoria_id == categoria_id)

        noticias = Noticia.query.filter(
            and_(*filters)
        ).paginate(page, offset, False)
        log.info("busca: {}".format(noticias.query.__dict__))

        pagination = {
            'page': noticias.page,
            'per_page': noticias.per_page,
            'total': noticias.total,
            'data': NoticiaSchema(many=True).dump(noticias.items)
        }

        #log.info("noticias: {}".format(pagination))
        # log.info("noticias: {}".format(noticias.query.__dict__))

        return jsonify(pagination), OK.value

    @jwt_required
    @restrict_access(['admin', 'editor', 'jornalista'])
    def post(self):
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        try:
            noticia = NoticiaSchema().load(data)
        except ValidationError as err:
            return NoticiaValidationErrorSchema().build(err.messages)

        noticia['categoria'] = Categoria.query.get(noticia['categoria_id'])

        if 'publicado' in noticia and noticia['publicado'] is True:
            noticia['data_publicacao'] = datetime.now()

        try:
            db.session.add(Noticia(**noticia))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during add noticia: {}".format(e))
            return InternalServerErrorSchema().build("Database Error")

        return NoticiaSchema().created(noticia)

    @jwt_required
    @restrict_access(['admin', 'editor', 'jornalista'])
    def put(self, noticia_id):
        noticia_id = int(noticia_id)
        categoria_id = None
        data = request.get_json()
        if not data or noticia_id is None:
            return EmptyDataSchema().build()

        noticia = Noticia.query.get(noticia_id)
        if not noticia:
            log.error('Noticia not found')
            return NoticiaNotFoundSchema().build()

        # todo: jornalista so edita a propria noticia

        try:
            new_noticia = NoticiaSchema().load(data)
        except ValidationError as err:
            log.error("Error while validate noticia: {}".format(err))
            return NoticiaValidationErrorSchema().build(err.message)

        categoria_id = new_noticia.get(categoria_id, None)

        if categoria_id:
            noticia['categoria'] = Categoria.query.get(categoria_id)

        noticia.update(**new_noticia)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update noticia: {}".format(e))
            return InternalServerErrorSchema().build()

        return NoticiaSchema().dump(noticia)

    @jwt_required
    @restrict_access(['admin', 'editor', 'jornalista'])
    def delete(self, noticia_id):
        noticia_id = int(noticia_id)

        noticia = Noticia.query.get(noticia_id)
        if not noticia:
            return NoticiaNotFoundSchema().build()

        # @TODO: jornalista so apaga a propria noticia

        try:
            db.session.delete(noticia)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during delete noticia: {}".format(e))
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value
