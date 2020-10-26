from ..app import db
from .abstract_user import AbstractUser
from werkzeug.security import generate_password_hash, check_password_hash


class HealthAuthority(db.Model):
    __tablename__ = "health_authority"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    phone = db.Column(db.Integer)

    country = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(128))
    city = db.Column(db.Unicode(128))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    # TODO this attributes are in common with the one of Operator and User, a refactor could be done
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False
