from .fixtures import app, client, db
from . import helpers
import os
from os.path import dirname

# !TO DO: this fails because of relative paths! need to find a way to fix this


def test_restaurants_map_is_correct(client, app):
    helpers.create_operator(client)
    helpers.login_operator(client)
    helpers.create_restaurant(client)
    path = os.path.join(dirname(app.root_path), 'monolith/templates/map.html')

    # in order to regenerate the map with test values
    res = client.get("/restaurants_map")

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        # checking restaurant details
        assert 'class="folium-map"' in text
        assert "Trattoria da Fabio" in text
        assert "40.720586" in text
        assert "10.1" in text
        assert "555123456"


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
