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


@home.route("/my_profile")
@login_required
def profile():
    if session["role"] == "authority":
        return redirect("/")
    elif session["role"] == "user":
        user = db.session.query(User).filter(
            User.id == current_user.id).first()
        return render_template("profile.html", user=user)
    elif session["role"] == "operator":
        user = db.session.query(Operator).filter(
            Operator.id == current_user.id).first()
        return render_template("profile.html", user=user)


@home.route("/my_profile/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            flash("Operation successful!")
        else:
            flash("You've input the wrong password!")

    return render_template("change_profile.html", form=form)


@ home.route("/my_profile/change_anagraphic", methods=["GET", "POST"])
@ login_required
def change_anagraphic():
    form = ChangeAnagraphicForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            if session["role"] == "user":
                current_user.firstname = form.firstname.data
            else:
                current_user.name = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.dateofbirth = form.dateofbirth.data
            current_user.fiscal_code = form.fiscal_code.data
            db.session.commit()
            flash("Operation successful!")
        else:
            flash("You've input the wrong password!")

    return render_template("change_profile.html", form=form)


@ home.route("/my_profile/change_contacts", methods=["GET", "POST"])
@ login_required
def change_contacts():
    form = ChangeContactForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.email = form.email.data
            current_user.phone_number = form.phone.data
            db.session.commit()
            flash("Operation successful!")
        else:
            flash("You've input the wrong password!")
    return render_template("change_profile.html", form=form)
