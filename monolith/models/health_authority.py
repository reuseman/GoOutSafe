from datetime import datetime
from monolith import db
from .abstract_user import AbstractUser
from . import Mark, User
from monolith.services.background import tasks

import logging

logger = logging.getLogger("monolith")


class HealthAuthority(AbstractUser):
    __tablename__ = "authority"
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

    marks = db.relationship("Mark", back_populates="authority")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def mark(self, user: User, duration=14, starting_date=datetime.utcnow()):
        logger.info(
            f"Authority (id={self.id}, name={self.name}) just marked the user (ID={user.id}, firstname={user.firstname})"
        )
        self.marks.append(
            Mark(user=user, authority=self, duration=duration, created=starting_date)
        )
        covid_19_positive_text = f"Hey {user.firstname},\nIn date {starting_date.strftime('%A %d. %B %Y')}, the health authority {self.name} marked you positive to Covid-19. Contact your personal doctor to protect your health and that of others."
        tasks.send_email(
            "You are positive to COVID-19",
            [user.email],
            covid_19_positive_text,
            covid_19_positive_text,
        )
