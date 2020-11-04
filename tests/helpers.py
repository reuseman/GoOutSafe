from datetime import date
from monolith.models.health_authority import HealthAuthority
from monolith.models.menu import Menu, Food
from monolith.models import User, Restaurant, RestaurantsPrecautions, HealthAuthority, Precautions
from monolith.services import mock
from tests.data import precautions

# DATA
# ! IMPORTANT
# FROM NOW ON LET'S PUT THE DEFINITION OF THE DATA IN tests/data.py, NOT HERE. IN ORDER TO HAVE A SINGLE TRUTH
# HERE ONLY THE METHODS

user = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth=date(1995, 12, 31),
    fiscal_code="RSSMRA95T31H501R",
    phone_number="+39331303313094",
)

user2 = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth="1995-12-31",
    fiscal_code="RSSMRA95T31H501R",
    phone_number="+39331303313094",
)

operator = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    dateofbirth="01/01/1963",
    fiscal_code="YLLGPP63A01B519O",
)

operator2 = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    dateofbirth="1963-01-01",
    fiscal_code="YLLGPP63A01B519O",
)

health_authority = dict(
    email="canicatti@asl.it",
    name="ASL Canicattì",
    password="cani123",
    phone="0808403849",
    country="Italy",
    state="AG",
    city="Canicattì",
    lat=37.36,
    lon=13.84,
)

health_authority2 = dict(
    email="roma@asl.it",
    name="ASL Roma",
    password="romasqpr",
    phone=" 0639741322",
    country="Italy",
    state="RM",
    city="Roma",
    lat=41.89,
    lon=12.49,
)

restaurant = dict(
    name="Trattoria da Fabio",
    phone=555123456,
    lat=40.720586,
    lon=10.10,
    time_of_stay=30,
    cuisine_type="ETHNIC",
    opening_hours=12,
    closing_hours=24,
    operator_id=1,
)


menu = dict(
    menu_name="Trial menu",
    name="Pepperoni pizza",
    price=5.0,
    category="PIZZAS"
)


table = dict(name="A10", seats=10, restaurant_id=1)


# CREATION


def create_user(client, data=user2):
    return client.post(
        "/create_user",
        data=data,
        follow_redirects=False,
    )


# ! It's here just as a reference. The testing procedure should not need to work directly
# !     with the database when a view to insert the user is available.
# TODO in the future if not needed, and the test goes as planned, it can be deleted.
def insert_user(db, data=user) -> User:
    temp = User(**data)
    db.session.add(temp)
    db.session.commit()
    return temp


def insert_restaurant_db(db, data=restaurant) -> Restaurant:
    temp = Restaurant(**data)
    db.session.add(temp)
    db.session.commit()
    return temp


def insert_precautions(db, precautions=precautions):
    for p in precautions:
        db.session.add(Precautions(**p))
    db.session.commit()


def insert_precautions_in_restaurant(db, restaurant: Restaurant, precautions_id=[1, 2, 4]):
    for precaution_id in precautions_id:
        db.session.add(RestaurantsPrecautions(restaurant_id=restaurant.id, precautions_id=precaution_id))
    db.session.commit()


def insert_complete_restaurant(db):
    restaurant = insert_restaurant_db(db)
    insert_precautions(db)
    insert_precautions_in_restaurant(db, restaurant=restaurant)
    return restaurant


def create_operator(client, data=operator2):
    return client.post(
        "/create_operator",
        data=data,
        follow_redirects=False,
    )


def create_health_authority(client, data=health_authority):
    return client.post(
        "/create_authority",
        data=data,
        follow_redirects=False,
    )


def create_restaurant(client, data=restaurant):
    return client.post(
        "/create_restaurant",
        data=data,
        follow_redirects=False,
    )


def create_menu(client, data=menu):
    return client.post(
        "/operator/restaurants/1/create_menu",
        data=data,
        follow_redirects=False,
    )


def show_menu(client, restaurant_id=1, menu_id=1):
    return client.get("/restaurants/" + str(restaurant_id) + "/show_menu/" + str(menu_id), follow_redirects=False)


def restaurant_sheet(client, restaurant_id=1):
    return client.get("/restaurants/" + str(restaurant_id), follow_redirects=False)


def operator_restaurants(client):
    return client.get("/operator/restaurants", follow_redirects=False)


def create_table(client, restaurant_id=1, data=table):
    return client.post(
        "/operator/restaurants/" + str(restaurant_id) + "/create_table",
        data=data,
        follow_redirects=False,
    )


def edit_table(client, restaurant_id=1, table_id=1, data=table):
    return client.post(
        "/operator/restaurants/"
        + str(restaurant_id)
        + "/tables/"
        + str(table_id)
        + "/edit_table",
        data=data,
        follow_redirects=False,
    )


def delete_table(client, restaurant_id=1, table_id=1, data=table):
    return client.post(
        "/operator/restaurants/"
        + str(restaurant_id)
        + "/tables/"
        + str(table_id)
        + "/delete_table",
        data=data,
        follow_redirects=False,
    )


def insert_health_authority(db, data=health_authority) -> HealthAuthority:
    temp = HealthAuthority(**data)
    db.session.add(temp)
    db.session.commit()
    return temp


# OTHER


def login_user(client, data=user):
    return client.post(
        "/login",
        data=data,
        follow_redirects=False,
    )


def login_operator(client, data=operator):
    return client.post(
        "/operator_login",
        data=data,
        follow_redirects=False,
    )


def logout_operator(client):
    return client.get(
        "/logout",
        follow_redirects=False,
    )


def login_authority(client, data=health_authority):
    return client.post(
        "/authority_login",
        data=data,
        follow_redirects=False,
    )
