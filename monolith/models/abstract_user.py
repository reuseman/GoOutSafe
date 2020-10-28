from ..app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class AbstractUser(UserMixin, db.Model):
    __abstract__ = True
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        if "password" in kw:
            self.password = generate_password_hash(kw.get("password"))
