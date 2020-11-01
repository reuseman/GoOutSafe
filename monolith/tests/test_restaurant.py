from .fixtures import app, client, db
from . import helpers
from ..models import Restaurant
from ..models.table import Table

from urllib.parse import urlparse

def test_create_restaurant_view_is_available_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get("/create_restaurant")
    assert res.status_code == 200


def test_create_restaurant_view_is_notavailable_anonymous(client):
    res = client.get("/create_restaurant")
    assert res.status_code == 401


def test_create_restaurant_view_is_notavailable_user(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/create_restaurant")
    assert res.status_code == 401


def test_create_restaurant_view_is_notavailable_ha(client):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/create_restaurant")
    assert res.status_code == 401


def test_create_restaurant(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    res = helpers.create_restaurant(client)

    fetched_restaurant = (
        db.session.query(Restaurant).filter_by(id=1, operator_id=1).first()
    )

    assert res.status_code == 302
    assert fetched_restaurant.name == "Trattoria da Fabio"
    assert fetched_restaurant.phone == 555123456
    assert fetched_restaurant.lat == 40.720586
    assert fetched_restaurant.lon == 10.10
    assert fetched_restaurant.time_of_stay == 30
    assert fetched_restaurant.operator.id == 1
    assert urlparse(res.location).path == "/operator/restaurants"


def test_create_restaurant_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)

    data = dict(
        name="Trattoria da Pippo", 
        phone=651981916,
        lat=-500.75,
        lon=900.98,
        time_of_stay=200,
        operator_id=1
    )

    res = helpers.create_restaurant(client, data)
    fetched_restaurant = (
        db.session.query(Restaurant).filter_by(operator_id=1).first()
    )

    assert fetched_restaurant is None
    assert res.status_code == 400


def test_create_duplicate_restaurant(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    data = dict(
        name="Trattoria da Fabio", 
        phone=4961,
        lat=40.720586,
        lon=10.10,
        time_of_stay=180,
        operator_id=1
    )

    res = helpers.create_restaurant(client, data)
    fetched_dup_restaurant = (
        db.session.query(Restaurant).filter_by(id=2).first()
    )

    assert res.status_code == 400
    assert fetched_dup_restaurant is None


def test_create_table_view_is_available_operator(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.insert_restaurant_db()
    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 200


def test_create_table_view_is_notavailable_anonymous(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db()
    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_user(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db()

    helpers.create_user(client)
    helpers.login_user(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_ha(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db()
    
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()

    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.create_table(client)
    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 302
    assert fetched_table.name == "A10"
    assert fetched_table.seats == 10
    assert urlparse(res.location).path == "/restaurants/1/tables"


def test_create_table_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    data = dict(
        name="A10",
        seats=-5,
        restaurant_id=1
    )
    res = helpers.create_table(client, data)

    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 400
    assert fetched_table is None


def test_create_duplicate_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)
    data = dict(
        name="A10",
        seats=2,
        restaurant_id=1
    )
    res = helpers.create_table(client, data)

    fetched_table = (
        db.session.query(Table).filter_by(id=2).first()
    )

    assert res.status_code == 400
    assert fetched_table is None


def test_create_table_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="01/01/1963",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.logout_operator(client)

    helpers.login_operator(client, data)
    res = helpers.create_table(client)
    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 400
    assert fetched_table is None


def test_delete_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)
    res = helpers.delete_table(client)

    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 302
    assert fetched_table is None


def test_delete_table_not_exists(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.delete_table(client)

    assert res.status_code == 400


def test_delete_table_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="01/01/1963",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout_operator(client)

    helpers.login_operator(client, data)
    res = helpers.delete_table(client)
    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 400
    assert fetched_table is not None


def test_delete_table_bad_table_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.delete_table(client, table_id=9)

    assert res.status_code == 400


def test_delete_table_bad_restaurant_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.delete_table(client, restaurant_id=5, table_id=1)

    assert res.status_code == 400


def test_edit_table(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)

    data = dict(
        id=1,
        name="A5",
        seats=6
    )
    res = helpers.edit_table(client, data=data)

    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 302
    assert fetched_table.name == "A5"
    assert fetched_table.seats == 6


def test_edit_table_to_one_with_same_name(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    helpers.create_table(client)

    data = dict(
        name="A5",
        seats=6
    )
    helpers.create_table(client, data=data)

    data["name"]="A10"
    data["seats"]=1
    res = helpers.edit_table(client, data)

    fetched_table = (
        db.session.query(Table).filter_by(id=2).first()
    )

    assert res.status_code == 400
    assert fetched_table.name == "A5"
    assert fetched_table.seats == 6


def test_edit_table_not_exists(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = helpers.edit_table(client)

    assert res.status_code == 400


def test_edit_table_not_owned_restaurant(client, db):
    helpers.create_operator(client)

    op_data = dict(
        email="pippo@lalocanda.com",
        firstname="pippo",
        lastname="pluto",
        password="5678",
        dateofbirth="01/01/1963",
        fiscal_code="UIBCAIUBBVX",
    )

    helpers.create_operator(client, op_data)

    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)
    helpers.logout_operator(client)

    helpers.login_operator(client, op_data)

    table_data = dict(
        id=1,
        name="A1",
        seats=1
    )
    res = helpers.edit_table(client, table_data)
    fetched_table = (
        db.session.query(Table).filter_by(id=1).first()
    )

    assert res.status_code == 400
    assert fetched_table.name != "A1"
    assert fetched_table.seats != 1


def test_edit_table_bad_restaurant_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.edit_table(client, restaurant_id=2)

    assert res.status_code == 400


def test_edit_table_bad_table_id(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    res = helpers.edit_table(client, table_id=2)

    assert res.status_code == 400


def test_edit_table_bad_data(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    bad_table = dict(
        name="A10",
        seats=-10
    )

    res = helpers.edit_table(client, data=bad_table)

    assert res.status_code == 400


def test_restaurants(client, db):
    helpers.insert_restaurant_db()
    allrestaurants = db.session.query(Restaurant).all()
    assert len(allrestaurants) == 1