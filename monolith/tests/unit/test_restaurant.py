import pytest

from ..fixtures import db, client, app
from ...models import Restaurant, Precautions, RestaurantsPrecautions, Operator
from ...models.table import Table
from ...controllers import restaurant
from .. import helpers


def test_add_new_restaurant_no_prec(client, db):
    helpers.create_operator(client)
    new_restaurant = Restaurant(**helpers.restaurant)

    res = restaurant.add_new_restaurant(new_restaurant)

    assert res == True
    assert db.session.query(Restaurant).filter_by(name=new_restaurant.name).first() is not None

def test_add_new_restaurant(client, db):
    helpers.create_operator(client)
    new_restaurant = Restaurant(**helpers.restaurant)

    res = restaurant.add_new_restaurant(new_restaurant, [1, 2])

    assert res == True
    assert db.session.query(Restaurant).filter_by(name=new_restaurant.name).first() is not None

def test_already_added_restaurant(client, db):
    helpers.create_operator(client)
    op = db.session.query(Operator).filter_by(id=1).first()
    new_restaurant1 = Restaurant(**helpers.restaurant)

    new_restaurant2 = Restaurant(
        name="Trattoria da Luca", 
        phone=651981916,
        lat=40.720586,
        lon=10.10,
        operator_id=op.id
    )

    restaurant.add_new_restaurant(new_restaurant1)
    res = restaurant.add_new_restaurant(new_restaurant2)

    assert res == False
    assert db.session.query(Restaurant).filter_by(name=new_restaurant2.name).first() is None

def test_add_new_table(client, db):
    helpers.create_operator(client)

    new_restaurant = Restaurant(**helpers.restaurant)
    restaurant.add_new_restaurant(new_restaurant)

    new_table = Table(**helpers.table)
    res = restaurant.add_new_table(new_table)

    assert res == True
    assert db.session.query(Table).filter_by(name=new_table.name).first() is not None

def test_already_added_table(client, db):
    helpers.create_operator(client)
    
    new_restaurant = Restaurant(**helpers.restaurant)
    restaurant.add_new_restaurant(new_restaurant)

    new_table1 = Table(**helpers.table)
    restaurant.add_new_table(new_table1)

    new_table2 = Table(
        name="A10",
        seats=5,
        restaurant_id=new_restaurant.id
    )
    res = restaurant.add_new_table(new_table2)

    assert res == False
    assert db.session.query(Table).filter_by(name=new_table2.name, seats=new_table2.seats).first() is None

def test_check_restaurant_ownership(client, db):
    helpers.create_operator(client)
    op1 = db.session.query(Operator).filter_by(id=1).first()
    helpers.create_operator(client)
    op2 = db.session.query(Operator).filter_by(id=2).first()

    new_restaurant = Restaurant(**helpers.restaurant)
    new_restaurant.operator_id = op1.id
    restaurant.add_new_restaurant(new_restaurant)

    res = restaurant.check_restaurant_ownership(op1.id, new_restaurant.id)
    assert res == True

    res = restaurant.check_restaurant_ownership(op2.id, new_restaurant.id)
    assert res == False
