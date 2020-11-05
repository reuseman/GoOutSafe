from faker import Faker
from codicefiscale import codicefiscale as cf
import datetime

from monolith import db
from monolith.views.health_authorities import _authorities
from monolith.models import (
    User,
    Operator,
    Restaurant,
    HealthAuthority,
    Precautions,
    RestaurantsPrecautions,
    Mark,
    Table,
    Booking,
)
from monolith.models.menu import Menu, Food

# ! IMPORTANT
# FROM NOW ON LET'S PUT THE DEFINITION OF THE DATA IN tests/data.py, NOT HERE. IN ORDER TO HAVE A SINGLE TRUTH

fake = Faker("it_IT")


def users(n=50):
    """
    Add a random number of users in the database, together with the default user.
    This method is not stable yet. Avoid using big numbers.

    Args:
        n (int, optional): Number of user to generate. Defaults to 50.
    """
    users_number = db.session.query(User).count()
    if users_number == 0:
        default_user()

        users = list()
        for i in range(0, n - 1):
            profile = fake.profile(["mail", "birthdate", "sex"])
            profile["first_name"] = fake.first_name()
            profile["last_name"] = fake.last_name()

            # Generate fiscal code
            # ! This is not a nice solution
            # TODO should be refactored
            fiscal_code = None
            while fiscal_code is None:
                try:
                    fiscal_code = cf.encode(
                        name=profile["first_name"],
                        surname=profile["last_name"],
                        sex=profile["sex"],
                        birthdate=profile["birthdate"].strftime("%d/%m/%Y"),
                        birthplace=fake.city(),
                    )
                except ValueError:
                    pass

            users.append(
                User(
                    email=profile["mail"],
                    firstname=profile["first_name"],
                    lastname=profile["last_name"],
                    phone_number=fake.phone_number().replace(" ", ""),
                    password=fake.password(length=fake.pyint(8, 24)),
                    dateofbirth=profile["birthdate"],
                    fiscal_code=fiscal_code,
                )
            )

        db.session.add_all(users)
        db.session.commit()


def default_user():
    q = db.session.query(User).filter(User.email == "example@example.com")
    user = q.first()
    if user is None:
        example = User(
            email="example@example.com",
            firstname="Admin",
            lastname="Admin",
            password="admin",
            dateofbirth=datetime.datetime(2020, 10, 5),
        )
        db.session.add(example)
        example = User(
            email="gino@pasticcino.com",
            firstname="Admin",
            lastname="Admin",
            password="admin",
            dateofbirth=datetime.datetime(2020, 10, 5),
        )
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
        example.password = "admin"
        example.fiscal_code = "my_fiscal_code"
        db.session.add(example)
        
        example = Operator()
        example.firstname = "OperatorAdmin"
        example.lastname = "OperatorAdmin"
        example.email = "operator1@example.com"
        example.dateofbirth = datetime.datetime(2020, 10, 9)
        example.is_admin = True
        example.password = "admin"
        example.fiscal_code = "my_fiscal_code"
        db.session.add(example)
        db.session.commit()


def health_authority():
    ha = (
        db.session.query(HealthAuthority)
        .filter(HealthAuthority.email == "auth@mail.com")
        .first()
    )
    if ha is None:
        example = HealthAuthority()
        example.name = "Admin"
        example.email = "auth@mail.com"
        example.password = "admin"
        example.phone = 3330049383
        example.country = "Italy"
        db.session.add(example)
        db.session.commit()


def restaurant():
    q = db.session.query(Restaurant).filter(Restaurant.id == 1)
    restaurant = q.first()
    if restaurant is None:
        db.session.add(
            Restaurant(
                name="Trial Restaurant",
                likes=42,
                phone=555123456,
                lat=43.720586,
                lon=10.408347,
                operator_id=1,
                time_of_stay=30,
                cuisine_type="ETHNIC",
                opening_hours=12,
                closing_hours=24,
            )
        )
        db.session.add(
            Restaurant(
                name="Trial Restaurant1",
                likes=42,
                phone=555123456,
                lat=44.720586,
                lon=10.408347,
                operator_id=1,
                time_of_stay=90,
                cuisine_type="FAST_FOOD",
                opening_hours=0,
                closing_hours=24,
            )
        )
        db.session.add(
            Restaurant(
                name="Trial Restaurant2",
                likes=42,
                phone=555123456,
                lat=43.720586,
                lon=9.408347,
                operator_id=1,
                time_of_stay=180,
                cuisine_type="PUB",
                opening_hours=19,
                closing_hours=5,
            )
        )
        db.session.commit()


def precautions():
    q = db.session.query(Precautions).filter(Precautions.id == 1)
    precautions = q.first()
    if precautions is None:
        db.session.add(Precautions(name="Amuchina"))
        db.session.add(Precautions(name="Social distancing"))
        db.session.add(Precautions(name="Disposable menu"))
        db.session.add(Precautions(name="Personnel required to wash hands regularly"))
        db.session.add(Precautions(name="Obligatory masks for staff in public areas"))
        db.session.add(Precautions(name="Tables sanitized at the end of each meal"))

        db.session.commit()


def restaurants_precautions():
    q = db.session.query(RestaurantsPrecautions).filter(
        RestaurantsPrecautions.restaurant_id == 1
    )
    restaurant_precautions = q.first()
    if restaurant_precautions is None:
        db.session.add(RestaurantsPrecautions(restaurant_id=1, precautions_id=1))
        db.session.add(RestaurantsPrecautions(restaurant_id=1, precautions_id=2))
        db.session.add(RestaurantsPrecautions(restaurant_id=2, precautions_id=1))
        db.session.add(RestaurantsPrecautions(restaurant_id=3, precautions_id=2))
        db.session.commit()


def mark_three_users():
    if not Mark.query.all():
        user1 = db.session.query(User).filter(User.id == 4).first()
        user2 = db.session.query(User).filter(User.id == 7).first()
        user3 = db.session.query(User).filter(User.id == 8).first()

        ha = db.session.query(HealthAuthority).filter(HealthAuthority.id == 1).first()
        ha.mark(user1)
        ha.mark(user2)
        ha.mark(user3)

        db.session.commit()


def table():
    q = db.session.query(Table).filter(Table.restaurant_id == 1)
    table = q.first()
    if table is None:
        db.session.add(Table(name="1", seats=5, restaurant_id=1))
        db.session.add(Table(name="2", seats=3, restaurant_id=1))
        db.session.add(Table(name="3", seats=3, restaurant_id=1))
        db.session.add(Table(name="4", seats=6, restaurant_id=1))
        db.session.add(Table(name="1", seats=10, restaurant_id=2))
        db.session.add(Table(name="2", seats=3, restaurant_id=2))
        db.session.add(Table(name="1", seats=2, restaurant_id=3))
        db.session.add(Table(name="2", seats=2, restaurant_id=3))
        db.session.commit()


def booking():
    booking = db.session.query(Booking).first()
    if booking is None:
        db.session.add(
            Booking(
                user_id=1,
                table_id=1,
                booking_number=1,
                start_booking=datetime.datetime.strptime(
                    str(datetime.date.today()) + " 8:00", "%Y-%m-%d %H:%M"
                ),
                end_booking=datetime.datetime.strptime(
                    str(datetime.date.today()) + " 8:30", "%Y-%m-%d %H:%M"
                ),
                confirmed_booking=True,
            )
        )
        db.session.add(
            Booking(
                user_id=1,
                table_id=7,
                booking_number=2,
                start_booking=datetime.datetime.strptime(
                    "2020-11-01 14:00", "%Y-%m-%d %H:%M"
                ),
                end_booking=datetime.datetime.strptime(
                    "2020-11-01 17:00", "%Y-%m-%d %H:%M"
                ),
                confirmed_booking=True,
            )
        )
        db.session.add(
            Booking(
                user_id=1,
                table_id=1,
                booking_number=3,
                start_booking=datetime.datetime.strptime(
                    "2020-10-01 8:00", "%Y-%m-%d %H:%M"
                ),
                end_booking=datetime.datetime.strptime(
                    "2020-10-01 8:30", "%Y-%m-%d %H:%M"
                ),
                confirmed_booking=True,
            )
        )
        db.session.commit()


def menu():
    q = db.session.query(Menu).filter(Menu.restaurant_id == 1)
    menu = q.first()
    if menu is None:
        menu = Menu(name="Trial Menu", restaurant_id=1)
        menu.foods.append(Food(name="Pepperoni pizza", price=5, category="PIZZAS"))
        menu.foods.append(Food(name="Water bottle", price=2, category="DRINKS"))

        db.session.add(menu)
        db.session.commit()


# TODO add review mock
