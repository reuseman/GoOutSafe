from ..app import db
from flask_login import UserMixin


class AbstractUser(UserMixin, db.Model):
    __abstract__ = True
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
