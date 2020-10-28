from ..app import db
from .abstract_user import AbstractUser
from werkzeug.security import generate_password_hash, check_password_hash


class User(AbstractUser):
    __tablename__ = "user"
    has_covid19 = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._authenticated = False

    @property
    def is_authenticated(self):
        return self._authenticated

    def get_id(self):
        return self.id
