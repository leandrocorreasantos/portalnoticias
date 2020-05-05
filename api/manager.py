import sys
import errno
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import app, db
from api.models import Categoria, Noticia


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    categorias = [
        {"id": 1, "nome": "Economia"},
        {"id": 2, "nome": "Política"},
        {"id": 3, "nome": "Moda"}
    ]
    for categoria in categorias:
        new_categoria = Categoria(**categoria)
        try:
            db.session.add(new_categoria)
            db.session.commit()
        except Exception as e:
            print("Erro ao cadastrar categoria: {}".format(e))

    agora = datetime.now()
    noticia = {
        "titulo": "Exemplo de Notícia",
        "conteudo": "Lorem ipsum dolor sit amet, consectetur adipisicing \
        elit. Facere ut officiis rerum, praesentium dolore dolor tempora \
        architecto accusamus, adipisci laudantium fugiat dolores fuga \
        odio minus! Quod accusantium necessitatibus quo rerum!",
        "publicado": True,
        "data_publicacao": agora,
        "meta_keywords": "lorem,ipsum",
        "meta_description": "Lorem Ipsum news"
    }

    for i in range(5):
        noticia["titulo"] = "Exemplo de Notícia {}".format(i + 1)
        new_noticia = Noticia(**noticia)
        try:
            db.session.add(new_noticia)
            db.session.commit()
        except Exception as e:
            print("Erro ao cadastrar noticia teste: {}".format(e))


if __name__ == '__main__':
    if not app.debug:
        print('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
