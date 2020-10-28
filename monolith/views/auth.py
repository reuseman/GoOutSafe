from flask import Blueprint, render_template, redirect, request, session, flash
from flask_login import current_user, login_user, logout_user, login_required

from monolith.app import db
from monolith.models import User, Operator, HealthAuthority
from ..services.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        user = db.session.query(User).filter(User.email == email).first()

        if user is not None and user.verify_password(password):
            login_user(user)
            # this sets the global role variable
            session["role"] = "user"
            session["name"] = user.firstname
            return redirect("/")
    return render_template("login.html", form=form, title="User Login")


@auth.route("/operator_login", methods=["GET", "POST"])
def operator_login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        operator = db.session.query(Operator).filter(Operator.email == email).first()

        if operator is not None and operator.verify_password(password):
            login_user(operator)
            # this sets the global role variable
            session["role"] = "operator"
            session["name"] = operator.firstname
            return redirect("/")
    return render_template("login.html", form=form, title="Operator Login")


@auth.route("/authority_login", methods=["GET", "POST"])
def authority_login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        authority = (
            db.session.query(HealthAuthority)
            .filter(HealthAuthority.email == email)
            .first()
        )

        if authority is not None and authority.verify_password(password):
            login_user(authority)
            # this sets the global role variable
            session["role"] = "authority"
            session["name"] = authority.name
            return redirect("/")
    return render_template("login.html", form=form, title="Authority Login")


@auth.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect("/")
