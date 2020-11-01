import pytest
import os
from flask import Flask

from monolith.views import blueprints
from monolith.services.auth import login_manager
from monolith.app import db as dba

from config import config


@pytest.yield_fixture
def app():
    app = Flask(__name__, template_folder="../monolith/templates")
    db_path = os.path.join(app.root_path, "gooutsafe_test.db")
    app.config.from_object(config["testing"])
    config["testing"].init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)

    dba.init_app(app=app)
    dba.create_all(app=app)

    context = app.app_context()
    context.push()

    yield app

    context.pop()
    # Teardown of the db
    dba.session.remove()
    dba.drop_all(app=app)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.yield_fixture
def db(app):
    yield dba
