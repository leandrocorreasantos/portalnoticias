from http.client import OK
from flask import jsonify
from flask.views import MethodView
from api.v1.schema import CategoriaSchema, NoticiaSchema
from api.models import Categoria, Noticia


class CategoriaView(MethodView):
    def get(self):
        categorias = Categoria.query.all()
        return jsonify(CategoriaSchema(many=True).dump(categorias)), OK.value


class NoticiaView(MethodView):
    def get(self):
        noticias = Noticia.query.all()
        return jsonify(NoticiaSchema(many=True).dump(noticias)), OK.value
