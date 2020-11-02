import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "top secret"
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY") or "top secret CSRF"
    SQLALCHEMY_DATABASE_URI = "sqlite:///gooutsafe.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = (
        os.environ.get("CELERY_BROKER_URL") or "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND = (
        os.environ.get("CELERY_RESULT_BACKEND") or "redis://localhost:6379/0"
    )

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):

    DEBUG = True

    @staticmethod
    def init_app(app):
        from flask_debugtoolbar import DebugToolbarExtension

        app.debug = True
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
