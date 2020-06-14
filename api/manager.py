import sys
import errno
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash

from api import app, db, log
from api.models import Role, User


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    categorias = [
        {"id": 1, "nome": "Economia"},
        {"id": 2, "nome": "Política"}
    ]

    for categoria in categorias:
        try:
            db.session.add(Categoria(**categoria))
            db.session.commit()
        except Exception as e:
            log.error("Erro ao cadastrar categoria: {}".format(e))

    noticias = [
        {"id": 1, "titulo": "noticia 1", "conteudo": "lorem ipsum dolor"},
        {"id": 2, "titulo": "noticia 2", "conteudo": "lorem ipsum dolor"},
        {"id": 3, "titulo": "noticia 3", "conteudo": "lorem ipsum dolor"},
    ]

    roles = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "editor"},
        {"id": 3, "name": "jornalista"},
    ]

    for role in roles:
        try:
            db.session.add(Role(**role))
            db.session.commit()
        except Exception as e:
            log.error("Erro ao cadastrar grupo: {}".format(e))

    admin = Role.query.get(1)

    user = {
        "id": 1,
        "username": "admin",
        "password": generate_password_hash("12345678"),
        "email": "admin@localhost",
        "first_name": "admin",
        "last_name": "admin",
        "roles": [admin]
    }

    try:
        db.session.add(User(**user))
        db.session.commit()
    except Exception as e:
        log.error("Erro ao adicionar usuario: {}".format(e))


if __name__ == '__main__':
    if not app.debug:
        log.error('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
