from gooutsafe import celery

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
