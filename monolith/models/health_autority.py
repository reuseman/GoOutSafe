from .abstract_user import AbstractUser

from ..app import db


class HealthAuthority(AbstractUser):
    __tablename__ = "authorities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128))
    name = db.Column(db.Unicode(128))
    password_hash = db.Column(db.Unicode(128))
    phone = db.Column(db.Integer)

    country = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(128))
    city = db.Column(db.Unicode(128))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
