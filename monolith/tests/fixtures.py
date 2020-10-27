import pytest
import os
import tempfile
from flask import Flask

from monolith.views import blueprints
from monolith.auth import login_manager

from monolith.app import db as dba


@pytest.fixture
def app():
    app = Flask(__name__, template_folder="../templates")
    db_path = os.path.join(app.root_path, "gooutsafe_test.db")

    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECRET_KEY"] = "my_secret_sqlite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DATABASE"] = db_path

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)

    dba.init_app(app=app)
    dba.create_all(app=app)

    context = app.app_context()
    context.push()

    yield app

    # Teardown of the db
    dba.session.remove()
    dba.drop_all(app=app)

    context.pop()

    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return dba
