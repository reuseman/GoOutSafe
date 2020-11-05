from datetime import date

user = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth=date(1995, 12, 31),
    fiscal_code="RSSMRA95T31H501R",
    phone_number="+39331303313094",
)

user2 = dict(
    email="mariobrown@gmail.com",
    firstname="mario",
    lastname="brown",
    password="1234",
    dateofbirth="1995-12-31",
    fiscal_code="RSSMRA95T31H501R",
    phone_number="+39331303313094",
)

operator = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    dateofbirth="01/01/1963",
    fiscal_code="YLLGPP63A01B519O",
    phone_number="+39331303313094",
)

operator2 = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    dateofbirth="1963-01-01",
    fiscal_code="YLLGPP63A01B519O",
    phone_number="+39331303313094",
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

health_authority2 = dict(
    email="roma@asl.it",
    name="ASL Roma",
    password="romasqpr",
    phone=" 0639741322",
    country="Italy",
    state="RM",
    city="Roma",
    lat=41.89,
    lon=12.49,
)

restaurant = dict(
    name="Trattoria da Fabio",
    phone=555123456,
    lat=40.720586,
    lon=10.10,
    time_of_stay=30,
    operator_id=1,
)

precaution1 = dict(name="Amuchina")
precaution2 = dict(name="Social distancing")
precaution3 = dict(name="Disposable menu")
precaution4 = dict(name="Personnel required to wash hands regularly")
precaution5 = dict(name="Obligatory masks for staff in public areas")
precaution6 = dict(name="Tables sanitized at the end of each meal")
precautions = [
    precaution1,
    precaution2,
    precaution3,
    precaution4,
    precaution5,
    precaution6,
]

table = dict(name="A10", seats=10, restaurant_id=1)


booking1 = dict(number_persons=1, booking_hour="8:00 - 8:30", booking_date=date.today(),)
booking1 = dict(number_persons=10, booking_hour="8:00 - 8:30", booking_date=date.today(),)
booking = [booking1]