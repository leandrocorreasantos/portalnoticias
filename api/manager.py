import sys
import errno
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import app, db
from api.models import Role, User


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    roles = [
        {"id": 1, "nome": "admin"},
        {"id": 1, "nome": "editor"},
        {"id": 1, "nome": "jornalista"},
    ]

    for role in roles:
        try:
            db.session.add(Role(role))
            db.session.commit()
        except Exception as e:
            print("Erro ao cadastrar grupo: {}".format(e))

    user = {
        "id": 1,
        "username": "admin",
        "password": "12345678",
        "email": "admin@localhost",
        "first_name": "admin",
        "last_name": "admin",
        "roles": [{"id": 1, "nome": "admin"}],
    }


if __name__ == '__main__':
    if not app.debug:
        print('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
