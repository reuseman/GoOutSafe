from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension  # debug

db = SQLAlchemy()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()


def create_app():
    app = Flask(__name__, static_folder="templates/assets")
    app.config["WTF_CSRF_SECRET_KEY"] = "my_secret"
    app.config["SECRET_KEY"] = "my_secret_sqlite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gooutsafe.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.debug = True  # debug

    context = app.app_context()
    context.push()

    from monolith.views import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)
    db.init_app(app)
    db.create_all(app=app)

    toolbar.init_app(app)  # debug

    from .services import mock

    mock.users(10)
    mock.operator()
    mock.restaurant()
    mock.precautions()
    mock.restaurants_precautions()
    # mock.health_authority()
    # mock.mark_three_users()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
