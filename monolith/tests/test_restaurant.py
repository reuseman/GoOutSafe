from .fixtures import app, client, db
from . import helpers
from ..models import Restaurant

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

    assert res.status_code == 400


def test_create_table_view_is_available_operator(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.inser_restaurant_db(db)
    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 200


def test_create_table_view_is_notavailable_anonymous(client, db):
    helpers.create_operator(client)
    helpers.inser_restaurant_db(db)
    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_user(client, db):
    helpers.create_operator(client)
    helpers.inser_restaurant_db(db)

    helpers.create_user(client)
    helpers.login_user(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_ha(client, db):
    helpers.create_operator(client)
    helpers.inser_restaurant_db(db)
    
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_restaurants(client, db):
    helpers.inser_restaurant_db(db)
    allrestaurants = db.session.query(Restaurant).all()
    assert len(allrestaurants) == 1