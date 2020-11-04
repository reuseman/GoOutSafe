from flask_mail import Message
from os import environ
from monolith import celery
from monolith import mail
from typing import List

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


@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task
def xsum(numbers):
    return sum(numbers)


# send_email("GoOutSafe - Notificaton", ["gooutsafe.squad2@gmail.com"],
# "Not a good news", "Not a good news (when you can render html)")
@celery.task
def send_email(
    subject,
    recipients: List[str],
    text_body,
    html_body,
    sender=environ.get("MAIL_USERNAME"),
    attachments=None,
):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    mail.send(msg)
