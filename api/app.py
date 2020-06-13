import os

from api import app as application
from api.v1.resources import CategoriasView as v1_Categorias
from api.v1.resources import NoticiasView as v1_Noticias
from api.v1.user_resources import UserView as v1_User
from api.v1.user_resources import LoginView as v1_Login



# module categoria
application.add_url_rule(
    '/v1/categorias',
    view_func=v1_Categorias.as_view('categorias'),
    methods=['GET']
)

application.add_url_rule(
    '/v1/categoria',
    view_func=v1_Categorias.as_view('categoria'),
    methods=['POST'])


# module user
application.add_url_rule(
    '/v1/user',
    view_func=v1_User.as_view('users'),
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/v1/user/<user_id>',
    view_func=v1_User.as_view('user'),
    methods=['PUT', 'DELETE']
)

application.add_url_rule(
    '/v1/user/login',
    view_func=v1_Login.as_view('login'),
    methods=['POST']
)

# module noticia

application.add_url_rule(
    '/v1/noticias',
    view_func=v1_Noticias.as_view('noticias'),
    methods=['GET']
)


if __name__ == '__main__':
    application.run(debug=application.debug,
                    host=os.environ.get('HOST', '0.0.0.0'),
                    port=int(os.environ.get('PORT', 5000)))
