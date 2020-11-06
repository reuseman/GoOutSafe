from flask import current_app
from flask_mail import Message
from os import environ
from monolith import celery as app
from monolith import mail, db
from typing import List
from config import Config
from celery.schedules import crontab
from monolith.models import User, Restaurant

"""
    Just as a reference 
    https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#project-layout
    https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html

    import the task that you want to execute from her

    if you do not care about the result, the broker of Celery will be contacted
    add.delay(4,10)

    if you care, than the broker and even the backend of Celery will be contacted
    res = add.delay(4,10) // res is an async result

"""


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        60.0,
        compute_restaurants_rating_average.s(),
        name="compute restaurants rating average",
    )

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s("world"), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s("Happy Mondays!"),
    # )


# @app.task
# def test(arg):
#     q = db.session.query(User).filter(User.id == 1).first()
#     print(q.firstname)
#     print(arg)


# @app.task
# def add(x, y):
#     return x + y


@app.task
def compute_restaurants_rating_average():
    restaurants = db.session.query(Restaurant).all()

    for restaurant in restaurants:
        reviews = restaurant.reviews
        average_rating = sum(review.rating for review in reviews)

        restaurant.average_rating = average_rating

    db.session.commit()


# send_email("GoOutSafe - Notificaton", ["gooutsafe.squad2@gmail.com"],
# "Not a good news", "Not a good news (when you can render html)")
@app.task
def send_email(
    subject,
    recipients: List[str],
    text_body,
    html_body,
    sender=Config.MAIL_SENDER,
    attachments=None,
):
    print(f"SENDING TO -> {recipients[0]}")
    print(f"sender: {sender}")
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    mail.send(msg)
