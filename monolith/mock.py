from monolith.app import db
from monolith.models import User, Operator, Restaurant

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
        db.session.add(example)
        db.session.commit()
