from ..app import db
from .abstract_user import AbstractUser


class User(AbstractUser):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password_hash = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    fiscal_code = db.Column(db.Unicode(128))
    has_covid19 = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
