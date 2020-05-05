import os

from api import app as application
from api.v1.resources import CategoriaView as v1_Categoria
from api.v1.resources import NoticiaView as v1_Noticia


#  This rule below is an example and can be removed.
application.add_url_rule(
    '/v1/categorias',
    view_func=v1_Categoria.as_view('categorias'),
    methods=['GET']
)

application.add_url_rule(
    '/v1/noticias',
    view_func=v1_Noticia.as_view('noticias'),
    methods=['GET']
)


if __name__ == '__main__':
    application.run(debug=application.debug,
                    host=os.environ.get('HOST', '0.0.0.0'),
                    port=int(os.environ.get('PORT', 5001)))
