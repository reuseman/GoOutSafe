from ..app import db
from .abstract_user import AbstractUser
from werkzeug.security import generate_password_hash, check_password_hash


class Operator(AbstractUser):
    __tablename__ = "operator"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fiscal_code = db.Column(db.Unicode(128))

    def __init__(self, *args, **kw):
        super(AbstractUser, self).__init__(*args, **kw)
        self._authenticated = False

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id