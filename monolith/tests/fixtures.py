import pytest

from monolith.app import create_app
from monolith.views import blueprints
from monolith.auth import login_manager


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECRET_KEY"] = "my_secret_sqlite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gooutsafe_test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from monolith.app import db

    context = app.app_context()
    context.push()

    db.init_app(app=app)
    db.create_all(app=app)

    yield db

    # Teardown of the db
    # TODO it would be nice to have the deletion of the created DB in the folder
    db.session.remove()
    db.drop_all(app=app)

    context.pop()
