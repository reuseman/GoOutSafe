from celery import Celery
from monolith import db
from monolith.models import User, Restaurant

BACKEND = BROKER = "redis://localhost:6379"
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def do_task():
    global _APP
    # lazy init
    if _APP is None:
        from monolith import create_app

        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    return []
