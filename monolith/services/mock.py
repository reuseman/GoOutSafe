from faker import Faker
from monolith.models import (
    User,
    Operator,
    Restaurant,
    HealthAuthority,
    Precautions,
    RestaurantsPrecautions,
    Table
)
from monolith.models.table import Table

import datetime

fake = Faker("it_IT")


def users(db,n=50):
    users_number = db.session.query(User).count()
    if users_number == 0:
        default_user(db)
        users = [
            User(
                email=fake.email(),
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                password=fake.password(length=fake.pyint(8, 24)),
                dateofbirth=fake.date_of_birth(minimum_age=16, maximum_age=86),
                has_covid19=False,
            )
            for i in range(0, n - 1)
        ]

        db.session.add_all(users)
        db.session.commit()


def default_user(db):
    q = db.session.query(User).filter(User.email == "example@example.com")
    user = q.first()
    if user is None:
        example = User(
            email="example@example.com",
            firstname="Admin",
            lastname="Admin",
            password="admin",
            dateofbirth=datetime.datetime(2020, 10, 5),
            has_covid19=False,
        )
        db.session.add(example)
        db.session.commit()


def operator(db):
    q = db.session.query(Operator).filter(Operator.email == "operator@example.com")
    user = q.first()
    if user is None:
        example = Operator()
        example.firstname = "OperatorAdmin"
        example.lastname = "OperatorAdmin"
        example.email = "operator@example.com"
        example.dateofbirth = datetime.datetime(2020, 10, 9)
        example.is_admin = True
        example.password = "admin"
        example.fiscal_code = "my_fiscal_code"
        db.session.add(example)
        db.session.commit()


def health_authority(db):
    q = db.session.query(HealthAuthority).filter(
        HealthAuthority.email == "auth@mail.com"
    )
    ha = q.first()
    if ha is None:
        example = HealthAuthority()
        example.name = "Admin"
        example.email = "auth@mail.com"
        example.password = "admin"
        example.phone = 3330049383
        example.country = "Italy"
        db.session.add(example)
        db.session.commit()


def restaurant(db):
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
        example.time_of_stay = 30
        db.session.add(example)
        db.session.commit()
    
def table(db):
    q = db.session.query(Table).filter(Table.id == 1)
    table = q.first()
    if table is None:
        example = Table()
        example.name = "A1"
        example.seats = 5
        example.restaurant_id = 1
        db.session.add(example)
        db.session.commit()


def precautions(db):
    q = db.session.query(Precautions).filter(Precautions.id == 1)
    precautions = q.first()
    if precautions is None:
        db.session.add(Precautions(name="Amuchina"))
        db.session.add(Precautions(name="Social distancing"))
        db.session.commit()


def restaurants_precautions(db):
    q = db.session.query(RestaurantsPrecautions).filter(
        RestaurantsPrecautions.restaurant_id == 1
    )
    restaurant_precautions = q.first()
    if restaurant_precautions is None:
        db.session.add(RestaurantsPrecautions(restaurant_id=1, precautions_id=1))
        db.session.add(RestaurantsPrecautions(restaurant_id=1, precautions_id=2))
        db.session.commit()


def table(db):
    q = db.session.query(Table).filter(
            Table.restaurant_id == 1
        )
    table = q.first()
    if table is None:
        db.session.add(Table(name="1", seats=5, restaurant_id=1))
        db.session.add(Table(name="2", seats=3, restaurant_id=1))
        db.session.commit()