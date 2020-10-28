from .models.table import Table
from monolith.app import db
from monolith.models import User, Operator, Restaurant, Precautions, RestaurantsPrecautions

import datetime


def user():
    q = db.session.query(User).filter(User.email == "example@example.com")
    user = q.first()
    if user is None:
        example = User()
        example.firstname = "Admin"
        example.lastname = "Admin"
        example.email = "example@example.com"
        example.dateofbirth = datetime.datetime(2020, 10, 5)
        example.is_admin = True
        example.set_password("admin")
        db.session.add(example)
        db.session.commit()


def operator():
    q = db.session.query(Operator).filter(Operator.email == "operator@example.com")
    user = q.first()
    if user is None:
        example = Operator()
        example.firstname = "OperatorAdmin"
        example.lastname = "OperatorAdmin"
        example.email = "operator@example.com"
        example.dateofbirth = datetime.datetime(2020, 10, 9)
        example.is_admin = True
        example.set_password("admin")
        example.fiscal_code = "my_fiscal_code"
        db.session.add(example)
        db.session.commit()


def restaurant():
    q = db.session.query(Restaurant).filter(Restaurant.id == 1)
    restaurant = q.first()
    if restaurant is None:
        example = Restaurant()
        example.name = "Trial Restaurant"
        example.likes = 42
        example.phone = 555123456
        example.lat = 43.720586
        example.lon = 10.408347
        example.operator_id = 1
        db.session.add(example)
        db.session.commit()


def precautions():
    q = db.session.query(Precautions).filter(Precautions.id == 1)
    precautions = q.first()
    if precautions is None:
        db.session.add(Precautions(name="Amuchina"))
        db.session.add(Precautions(name="Social distancing"))
        db.session.commit()


def table():
    q = db.session.query(Table).filter(Table.id == 1)
    table = q.first()
    if table is None:
        db.session.add(Table(name="A1", seats=5, restaurant_id=1))
        db.session.add(Table(name="B4", seats=10, restaurant_id=1))
        db.session.commit()

def restaurants_precautions():
    q = db.session.query(RestaurantsPrecautions).filter(RestaurantsPrecautions.restaurant_id == 1)
    restaurant_precautions = q.first()
    if restaurant_precautions is None:
        db.session.add(RestaurantsPrecautions(restaurant_id=1, precautions_id=1))
        db.session.add(RestaurantsPrecautions(restaurant_id=1, precautions_id=2))
        db.session.commit()