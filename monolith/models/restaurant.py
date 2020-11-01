from ..app import db
from .table import Table


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text(100))

    likes = db.Column(
        db.Integer
    )  # will store the number of likes, periodically updated in background

    lat = db.Column(db.Float)  # restaurant latitude
    lon = db.Column(db.Float)  # restaurant longitude

    phone = db.Column(db.Integer)
    time_of_stay = db.Column(db.Integer)  # minutes
    operator_id = db.Column(db.Integer, db.ForeignKey("operator.id"))

    tables = db.relationship("Table", backref="restaurant")
    reviews = db.relationship("Review", back_populates="restaurant")
