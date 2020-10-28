from ..models import User

# DATA

user = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth="31/12/1995",
    has_covid19=False,
)

operator = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    dateofbirth="01/01/1963",
    fiscal_code="YLLGPP63A01B519O",
)

health_authority = dict(
    email="canicatti@asl.it",
    name="ASL Canicattì",
    password="cani123",
    phone="0808403849",
    country="Italy",
    state="AG",
    city="Canicattì",
    lat=37.36,
    lon=13.84,
)

# CREATION


def create_user(client, data=user):
    return client.post(
        "/create_user",
        data=data,
        follow_redirects=False,
    )


# ! It's here just as a reference. The testing procedure should not need to work directly
# !     with the database when a view to insert the user is available.
# TODO in the future if not needed, and the test goes as planned, it can be deleted.
def insert_user(db, data=user) -> User:
    temp = User(**data)
    db.session.add(temp)
    db.session.commit()
    return temp


def create_operator(client, data=operator):
    return client.post(
        "/create_operator",
        data=data,
        follow_redirects=False,
    )


def create_health_authority(client, data=health_authority):
    return client.post(
        "/create_authority",
        data=data,
        follow_redirects=False,
    )


# OTHER


def login_user(client, data=user):
    return client.post(
        "/login",
        data=data,
        follow_redirects=False,
    )


def login_operator(client, data=operator):
    return client.post(
        "/operator_login",
        data=operator,
        follow_redirects=False,
    )


def login_authority(client, data=health_authority):
    return client.post(
        "/authority_login",
        data=data,
        follow_redirects=False,
    )
