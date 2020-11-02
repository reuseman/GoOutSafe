# DOT ENV
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# APP
from monolith import create_app
from monolith.services.background.celery import make_celery

app = create_app(os.getenv("FLASK_CONFIG") or "default")
celery = make_celery(app)
