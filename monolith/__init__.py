from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    context = app.app_context()
    context.push()

    from monolith.views import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)
    db.init_app(app)
    db.create_all(app=app)

    from .services import mock

    mock.users(10)
    mock.operator()
    mock.restaurant()
    mock.menu()
    mock.table()
    mock.precautions()
    mock.restaurants_precautions()
    mock.health_authority()
    mock.mark_three_users()

    return app
