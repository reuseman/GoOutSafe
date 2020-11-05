from flask import Blueprint, render_template, session, redirect, request
from flask_login import login_required
from flask.helpers import flash

from monolith import db
from monolith.models import Restaurant, User, Operator
from monolith.services.auth import current_user
from monolith.services.forms import (
    ChangePasswordForm,
    ChangeAnagraphicForm,
    ChangeContactForm,
)


home = Blueprint("home", __name__)


@home.route("/")
def index():
    return render_template("index.html")
