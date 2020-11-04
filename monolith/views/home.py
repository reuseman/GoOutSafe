from flask import Blueprint, render_template, session, redirect
from flask_login import login_required

from monolith import db
from monolith.models import Restaurant, Like, User
from monolith.services.auth import current_user

home = Blueprint("home", __name__)


@home.route("/")
def index():
    if current_user is not None and hasattr(current_user, "id"):
        restaurants = db.session.query(Restaurant)
    else:
        restaurants = None
    return render_template("index.html", restaurants=restaurants)


@home.route("/my_profile")
@login_required
def profile():
    if session["role"] == "authority":
        return redirect("/")
    elif session["role"] == "user":
        user = db.session.query(User).filter(
            User.id == current_user.id).first()
        return render_template("profile.html", user=user)
