import sys
import errno
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash

from api import app, db
from api.models import Role, User, UserRoles


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
            db.session.rollback()
            print("Erro ao cadastrar grupo: {}".format(e))

    user = {
        "id": 1,
        "username": "admin",
        "password": generate_password_hash("12345678"),
        "email": "admin@localhost",
        "first_name": "admin",
        "last_name": "admin",
    }

    try:
        db.session.add(User(**user))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Erro ao cadastrar administrador: {}".format(e))

    userroles = {"id": 1, "user_id": 1, "role_id": 1}
    try:
        db.session.add(UserRoles(**userroles))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Erro ao cadastrar relacionamento: {}".format(e))


if __name__ == '__main__':
    if not app.debug:
        print('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
