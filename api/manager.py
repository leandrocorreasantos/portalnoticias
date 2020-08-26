import sys
import errno
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import app, db, log
from api.models import Role, User
from werkzeug.security import generate_password_hash


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
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
            db.session.rollback()

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
        db.session.rollback()


if __name__ == '__main__':
    if not app.debug:
        log.error('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
