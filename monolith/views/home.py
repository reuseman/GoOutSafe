from flask import Blueprint, render_template, session, redirect, request
from flask_login import login_required
from flask.helpers import flash

from monolith import db
from monolith.models import Restaurant, Like, User, Operator
from monolith.services.auth import current_user
from monolith.services.forms import (
    ChangePasswordForm,
    ChangeAnagraphicForm,
    ChangeContactForm,
)


home = Blueprint("home", __name__)


@home.route("/")
def index():
    if current_user is not None and hasattr(current_user, "id"):
        restaurants = db.session.query(Restaurant)
    else:
        restaurants = None
    return render_template("index.html", restaurants=restaurants)
