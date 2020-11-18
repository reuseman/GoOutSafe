import os
from logging import FileHandler, Formatter
from logging.config import dictConfig

fileHandler = FileHandler("monolith/monolith.log", encoding="utf-8")
fileHandler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "top secret"
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY") or "top secret CSRF"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///gooutsafe.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = [".jpg", ".png", ".gif"]
    UPLOAD_PATH = "uploads"

    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = ".png, .jpg, .jpeg"
    DROPZONE_MAX_FILE_SIZE = 2
    DROPZONE_MAX_FILES = 30
    DROPZONE_UPLOAD_MULTIPLE = True
    DROPZONE_UPLOAD_ON_CLICK = True

    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = os.environ.get("MAIL_PORT") or 8025
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or None
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or None
    MAIL_SENDER = os.environ.get("MAIL_SENDER") or "no-reply@gooutsafe.com"

    # https://avatars.dicebear.com/api/avataaars/roma%20molesta.svg
    AVATAR_PROVIDER = "https://avatars.dicebear.com/api/avataaars/{seed}.svg"

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = (
        os.environ.get("CELERY_RESULT_BACKEND") or "redis://redis:6379/0"
    )
    CELERY_TASKS = ["monolith.services.background.tasks"]

    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    FLASK_PROFILER_ADMIN = os.environ.get("FLASK_PROFILER_USERNAME") or "admin"
    FLASK_PROFILER_PASSWORD = os.environ.get("FLASK_PROFILER_USERNAME") or "password"
    FLASK_PROFILER = {
        "enabled": True,
        "storage": {"engine": "sqlite"},
        "basicAuth": {
            "enabled": True,
            "username": FLASK_PROFILER_ADMIN,
            "password": FLASK_PROFILER_PASSWORD,
        },
        "ignore": ["^/static/.*"],
    }

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    @staticmethod
    def init_app(app):
        app.logger.addHandler(fileHandler)


class DevelopmentConfig(Config):

    DEBUG = True

    @staticmethod
    def init_app(app):
        from flask_debugtoolbar import DebugToolbarExtension

        app.debug = True
        app.logger.addHandler(fileHandler)
        DebugToolbarExtension(app)


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///gooutsafe_test.db"
    )


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig,
}

mail_body_covid_19_mark = "Hey {},\nIn date {}, the health authority {} marked you positive to Covid-19. Contact your personal doctor to protect your health and that of others."
mail_body_covid_19_contact = "Hey {},\nIn date {}, while you were at restaurant {}, you could have been in contact with a Covid-19 case. Contact your personal doctor to protect your health and that of others."
mail_body_covid_19_operator_alert = "Hey {},\nIn date {}, at your restaurant {}, a Covid-19 case had a booking. Execute as soon as possible the health protocols."
mail_body_covid_19_operator_booking_alert = "Hey {},\nYou have a booking of a Covid-19 positive case, at your restaurant {}. The reservation ID is {} at table {}."
