from flask import Blueprint, render_template, session, redirect
from flask_login import login_required
from flask.helpers import flash

from monolith import db
from monolith.models import User, Operator
from monolith.services.auth import current_user
from monolith.services.forms import (
    ChangePasswordForm,
    ChangeAnagraphicForm,
    ChangeContactForm,
)

me = Blueprint("me", __name__)


@me.route("/me")
@login_required
def profile():
    if session["role"] == "authority":
        return redirect("/")
    elif session["role"] == "user":
        user = db.session.query(User).filter(User.id == current_user.id).first()
        return render_template("profile.html", user=user)
    elif session["role"] == "operator":
        user = db.session.query(Operator).filter(Operator.id == current_user.id).first()
        return render_template("profile.html", user=user)


@me.route("/me/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            flash("Operation successful!")
        else:
            flash("You've typed the wrong password!")

    return render_template("change_profile.html", form=form)


@me.route("/me/change_anagraphic", methods=["GET", "POST"])
@login_required
def change_anagraphic():
    form = ChangeAnagraphicForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.dateofbirth = form.dateofbirth.data
            current_user.fiscal_code = form.fiscal_code.data
            db.session.commit()
            flash("Operation successful!")
        else:
            flash("You've typed the wrong password!")

    return render_template("change_profile.html", form=form)


@me.route("/me/change_contacts", methods=["GET", "POST"])
@login_required
def change_contacts():
    form = ChangeContactForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.email = form.email.data
            current_user.phone_number = form.phone.data
            db.session.commit()
            flash("Operation successful!")
        else:
            flash("You've typed the wrong password!")
    return render_template("change_profile.html", form=form)
