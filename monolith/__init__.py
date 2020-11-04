from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# from flask_celeryext import FlaskCeleryExt
from config import config, Config
from celery import Celery

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


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
    mail.init_app(app)
    celery.conf.update(app.config)

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
    mock.booking()

    app.logger.info("Server startup")

    # # Prova mail
    # from flask_mail import Message

    # msg = Message(
    #     "test subject",
    #     sender="gooutsafe.squad2@gmail.com",
    #     recipients=["gooutsafe.squad2@gmail.com"],
    # )
    # msg.body = "text body"
    # msg.html = "<h1>HTML body</h1>"
    # mail.send(msg)
    return app
