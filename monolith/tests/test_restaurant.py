from .fixtures import app, client, db
from . import helpers
from ..models import Restaurant

def test_restaurants(client, db):
    helpers.inser_restaurant_db(db)
    allrestaurants = db.session.query(Restaurant).all()
    assert len(allrestaurants) == 1