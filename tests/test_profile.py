from .fixtures import app, client, db
from . import helpers


def test_my_profile_view_is_available_for_user(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/my_profile")

    assert res.status_code == 200


def test_my_profile_view_is_available_for_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get("/my_profile")

    assert res.status_code == 200


def test_my_profile_view_is_correct_for_user(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/my_profile")

    assert b"mariobrown@gmail.com" in res.data
    assert b"mario" in res.data
    assert b"brown" in res.data
    assert b"RSSMRA95T31H501R" in res.data


def test_my_profile_view_is_correct_for_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.get("/my_profile")

    assert b"giuseppebrown@lalocanda.com" in res.data
    assert b"giuseppe" in res.data
    assert b"yellow" in res.data
    assert b"YLLGPP63A01B519O" in res.data


def test_my_profile_view_not_available_for_unlogged_users(client):

    res = client.get("/my_profile")

    assert res.status_code == 401


def test_my_profile_view_redirects_authority(client):
    helpers.create_health_authority(client)
    helpers.login_authority(client)

    res = client.get("/my_profile")

    assert res.status_code == 302


def test_profile_forms_are_available(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res1 = client.get("/my_profile/change_password")
    res2 = client.get("/my_profile/change_anagraphic")
    res3 = client.get("/my_profile/change_contacts")

    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res3.status_code == 200


def test_password_form(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.post(
        "/my_profile/change_password",
        data=dict(
            new_password="5678",
            password_confirm="5678",
            old_password="1234",
        ),
        follow_redirects=False,
    )

    assert res.status_code == 200

    helpers.logout

    res = client.post(
        "/login",
        data=dict(
            email="mariobrown@gmail.com",
            password="5678",
        ),
        follow_redirects=False,
    )
    assert res.status_code == 302


def test_anagraphic_form_user(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.post(
        "/my_profile/change_anagraphic",
        data=dict(
            firstname="Hattori",
            lastname="Hanzo",
            fiscal_code="HTTHNZ45B02D612A",
            dateofbirth="1945-02-02",
            password="1234",
        ),
        follow_redirects=False,
    )

    assert res.status_code == 200

    res = client.get("/my_profile")
    assert b"Hattori" in res.data
    assert b"Hanzo" in res.data
    assert b"HTTHNZ45B02D612A" in res.data


def test_anagraphic_form_operator(client):
    helpers.create_operator(client)
    helpers.login_operator(client)

    res = client.post(
        "/my_profile/change_anagraphic",
        data=dict(
            firstname="O-Ren",
            lastname="Ishii",
            fiscal_code="RNXSHX74C03D612A",
            dateofbirth="1945-03-03",
            password="5678",
        ),
        follow_redirects=False,
    )

    assert res.status_code == 200

    res = client.get("/my_profile")
    assert b"O-Ren" in res.data
    assert b"Ishii" in res.data
    assert b"RNXSHX74C03D612A" in res.data


def test_contact_form(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.post(
        "/my_profile/change_contacts",
        data=dict(
            email="hattori@katanas.jp",
            phone="+81855696969",
            password="1234",
        ),
        follow_redirects=False,
    )

    assert res.status_code == 200

    res = client.get("/my_profile")
    assert b"hattori@katanas.jp" in res.data


def test_wrong_password_in_forms(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res1 = client.post(
        "/my_profile/change_password",
        data=dict(
            new_password="PaiMei",
            password_confirm="PaiMei",
            old_password="Budd",
        ),
        follow_redirects=False,
    )

    res2 = client.post(
        "/my_profile/change_anagraphic",
        data=dict(
            firstname="Hattori",
            lastname="Hanzo",
            fiscal_code="HTTHNZ45B02D612A",
            dateofbirth="1945-02-02",
            password="BeatrixKiddo",
        ),
        follow_redirects=False,
    )

    res3 = client.post(
        "/my_profile/change_contacts",
        data=dict(
            email="hattori@katanas.jp",
            phone="+81855696969",
            password="ElleDriver",
        ),
        follow_redirects=False,
    )

    assert (res1.status_code == 200)
    assert (res2.status_code == 200)
    assert (res3.status_code == 200)


def test_form_iframes_in_view(client):
    helpers.create_user(client)
    helpers.login_user(client)

    res = client.get("/my_profile")

    assert b"password_iframe" in res.data
    assert b"anagraphic_iframe" in res.data
    assert b"contacts_iframe" in res.data
