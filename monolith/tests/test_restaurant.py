from .fixtures import app, client, db
from . import helpers
from ..models import Restaurant

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


def test_create_table_view_is_available_operator(client, db):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.insert_restaurant_db(db)
    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 200


def test_create_table_view_is_notavailable_anonymous(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db(db)
    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_user(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db(db)

    helpers.create_user(client)
    helpers.login_user(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_create_table_view_is_notavailable_ha(client, db):
    helpers.create_operator(client)
    helpers.insert_restaurant_db(db)
    
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    q = db.session.query(Restaurant).filter_by(id=1).first()
    
    res = client.get("/operator/restaurants/" + str(q.id) + "/create_table")
    assert res.status_code == 401


def test_restaurants(client, db):
    helpers.insert_restaurant_db(db)
    allrestaurants = db.session.query(Restaurant).all()
    assert len(allrestaurants) == 1