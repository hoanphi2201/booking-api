import flask_migrate as _fm
import flask_sqlalchemy as _fs

db = _fs.SQLAlchemy()
migrate = _fm.Migrate(db=db)


def init_app(app, **kwargs):
    db.app = app
    migrate.init_app(app)
    db.init_app(app)


from .hotel import Hotel