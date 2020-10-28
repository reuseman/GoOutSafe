from ..app import db
from .abstract_user import AbstractUser
from werkzeug.security import generate_password_hash, check_password_hash


class Operator(AbstractUser):
    __tablename__ = "operator"
    fiscal_code = db.Column(db.Unicode(128))

    restaurants = db.relationship("Restaurant", backref="operator")

    def __init__(self, *args, **kw):
        super(AbstractUser, self).__init__(*args, **kw)
        self._authenticated = False

    @property
    def is_authenticated(self):
        return self._authenticated

    def get_id(self):
        return self.id
