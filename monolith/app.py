from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder="templates/assets")
    app.config["WTF_CSRF_SECRET_KEY"] = "my_secret"
    app.config["SECRET_KEY"] = "my_secret_sqlite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gooutsafe.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from monolith.views import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)

    db.init_app(app)
    db.create_all(app=app)

    from .services import mock

    mock.users()
    mock.operator()
    mock.restaurant()
    mock.precautions()
    mock.restaurants_precautions()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
