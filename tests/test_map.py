from .fixtures import app, client, db
from . import helpers
import os
from os.path import dirname


def test_restaurants_map_is_correct(client, app):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    # in order to regenerate the map with test values
    res = client.get("/restaurants_map")

    assert b'Trattoria da Fabio' in res.data
    assert b'40.720586' in res.data
    assert b'10.1' in res.data
    assert b'555123456' in res.data


def test_restaurants_map_view_is_available(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/restaurants_map")

    assert res.status_code == 200


def test_map_is_in_view(client):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)

    res = client.get("/restaurants_map")

    assert b'id="map"' in res.data
