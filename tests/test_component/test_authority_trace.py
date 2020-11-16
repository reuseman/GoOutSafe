from ..fixtures import app, db, client
from .. import helpers
from ..data import booking_people, user2, user3


def test_ha_should_access_own_trace_page(client):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get(
        "trace",
        follow_redirects=False,
    )

    assert res.status_code == 200


def test_ha_should_trace_through_user_customer_same_time(client, db):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    helpers.create_operator(client)
    helpers.create_restaurant(client)
    helpers.create_table(client)

    helpers.login_user(client)
    helpers.booking(client)
    helpers.checkin_booking(client)

    helpers.login_user(client, data=user3)
    helpers.booking_multiple_user(client)
    helpers.booking_confirm(client)
    helpers.checkin_booking_multiple_user(client)
    helpers.logout(client)

    res = client.post(
        "trace",
        data={"identifier": user2["fiscal_code"], "duration": 14},
        follow_redirects=True,
    )

    assert res.status_code == 200
    assert b"Traced contacts" in res.data
    # for value in booking_people.values():
    #     assert bytes(value, "utf-8") in res.data


def test_operator_should_not_access_trace_page(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get(
        "trace",
        follow_redirects=False,
    )

    assert res.status_code == 401


def test_user_should_not_access_trace_page(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get(
        "trace",
        follow_redirects=False,
    )

    assert res.status_code == 401


def test_anonymous_should_not_access_trace_page(client):
    res = client.get(
        "trace",
        follow_redirects=False,
    )

    assert res.status_code == 302
