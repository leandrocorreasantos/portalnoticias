import os

from api import app as application
from api.v1.resources import CategoriasView as v1_Categorias
from api.v1.resources import NoticiasView as v1_Noticias


#  This rule below is an example and can be removed.
application.add_url_rule(
    '/v1/categoria',
    view_func=v1_Categorias.as_view('categorias'),
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/v1/categoria/<categoria_id>',
    view_func=v1_Categorias.as_view('categoria'),
    methods=['PUT', 'DELETE']
)

application.add_url_rule(
    '/v1/noticias',
    view_func=v1_Noticias.as_view('noticias'),
    methods=['GET']
)


if __name__ == '__main__':
    application.run(debug=application.debug,
                    host=os.environ.get('HOST', '0.0.0.0'),
                    port=int(os.environ.get('PORT', 5000)))
