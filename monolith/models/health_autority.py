from flask_login import UserMixin

from ..app import db
from werkzeug.security import generate_password_hash, check_password_hash


class HealthAuthority(UserMixin, db.Model):
    __tablename__ = "authorities"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    password_hash = db.Column(db.Unicode(128))
    phone = db.Column(db.Integer)

    country = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(128))
    city = db.Column(db.Unicode(128))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def get_id(self):
        return self.id
