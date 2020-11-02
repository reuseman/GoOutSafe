from .fixtures import app, client, db
from . import helpers

# !TO DO: this fails because of relative paths! need to find a way to fix this


def test_restaurants_map_is_correct(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/map.html")
    # checking restaurant details
    assert b"Trattoria da Fabio" in res.data
    assert b"555123456" in res.data
    assert b"40.720586" in res.data
    assert b"10.10" in res.data


def test_restaurants_map_view_is_available(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/restaurants_map")

    assert res.status_code == 200


def test_map_iframe_is_in_view(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/restaurants_map")

    assert b"restaurants_map" in res.data
