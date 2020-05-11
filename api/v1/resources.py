from http.client import OK
from flask import jsonify
from flask.views import MethodView
from api import log, db
from api.v1.schema import (
    CategoriaSchema, NoticiaSchema,
    CategoriaValidationErrorSchema
)
from api.models import Categoria, Noticia


class CategoriasView(MethodView):
    def get(self):
        categorias = Categoria.query.all()
        return jsonify(CategoriaSchema(many=True).dump(categorias)), OK.value

    def post(self):
        try:
    	   categoria = CategoriaSchema().load(request.get_json())
        except ValidationError as err:
            return CategoriaValidationErrorSchema().build(err.messages)

    	new_categoria = Categoria(**categoria)
    	try:
    		db.session.add(new_categoria)
    		db.session.commit()
    	except Exception as e:
    		log.error("Erro ao cadastrar categoria: {}".format(e))

    	return CategoriaSchema().build(new_categoria)


class NoticiasView(MethodView):
    def get(self):
        noticias = Noticia.query.all()
        return jsonify(NoticiaSchema(many=True).dump(noticias)), OK.value


    def post(self):
    	noticia = NoticiaSchema().load(request.get_json())
    	new_noticia = Noticia(**noticia)
    	try:
    		db.session.add(new_noticia)
    		db.session.commit()
    	except Exception as e:
    		log.error("Erro ao cadastrar notícia: {}".format(e))

    	return NoticiaSchema().build(new_noticia)
