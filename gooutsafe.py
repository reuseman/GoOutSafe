# DOT ENV
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# APP
from monolith import create_app, celery

app = create_app(os.getenv("FLASK_CONFIG") or "default")

# Shell

from monolith import db
from monolith.models import (
    User,
    Review,
    Operator,
    Restaurant,
    RestaurantsPrecautions,
    Precautions,
    Table,
    Mark,
    HealthAuthority,
    Booking,
)
from monolith.services.background import tasks


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "tasks": tasks,
        "User": User,
        "Review": Review,
        "Operator": Operator,
        "Restaurant": Restaurant,
        "RestaurantsPrecautions": RestaurantsPrecautions,
        "Precautions": Precautions,
        "Table": Table,
        "Mark": Mark,
        "HealthAuthority": HealthAuthority,
        "Booking": Booking,
    }
