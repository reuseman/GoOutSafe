from flask_login import UserMixin

from ..app import db
from werkzeug.security import generate_password_hash, check_password_hash


class HealthAuthority(UserMixin, db.Model):
    __tablename__ = "authorities"
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

    def __init__(self, *args, **kw):
        if "password" in kw:
            self.password = generate_password_hash(kw.get("password"))

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id
