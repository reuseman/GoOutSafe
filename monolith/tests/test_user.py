from .fixtures import app, client, db
from monolith.models import User

from urllib.parse import urlparse
import datetime


def test_create_user_view_is_available(client):
    res = client.get("/create_user")
    assert res.status_code == 200


def test_create_user_view(client, db):
    res = add_user(client)

    fetched_user = (
        db.session.query(User).filter(User.email == "mariorossi@mail.com").first()
    )

    assert res.status_code == 302
    assert fetched_user.email == "mariorossi@mail.com"
    assert fetched_user.firstname == "mario"
    assert fetched_user.lastname == "rossi"
    assert fetched_user.dateofbirth == datetime.datetime(2020, 12, 5)
    assert urlparse(res.location).path == "/users"


def test_correct_login(client):
    add_user(client)

    res = client.post(
        "/login",
        data=dict(
            email="mariorossi@mail.com",
            password="1233454",
        ),
        follow_redirects=False,
    )

    assert res.status_code == 302


# Helpers methods


def add_user(client):
    return client.post(
        "/create_user",
        data=dict(
            email="mariorossi@mail.com",
            firstname="mario",
            lastname="rossi",
            dateofbirth="05/12/2020",
            password="1233454",
        ),
        follow_redirects=False,
    )
