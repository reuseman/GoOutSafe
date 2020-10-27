from flask import Blueprint, render_template, redirect, request, session, flash
from flask_login import current_user, login_user, logout_user, login_required

from monolith.app import db
from monolith.models import User, Operator, HealthAuthority
from monolith.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        print(email)
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        print(q.first().id)
        if user is not None and user.authenticate(password):
            login_user(user)
            # this sets the global role variable
            session["role"] = "user"
            return redirect("/")
    return render_template("login.html", form=form)


@auth.route("/operator_login", methods=["GET", "POST"])
def operator_login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        q = db.session.query(Operator).filter(Operator.email == email)
        operator = q.first()
        print(q.first().id)
        if operator is not None and operator.authenticate(password):
            login_user(operator)
            # this sets the global role variable
            session["role"] = "operator"
            return redirect("/")
    return render_template("login.html", form=form)


@auth.route("/authority_login", methods=["GET", "POST"])
def authority_login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        q = db.session.query(HealthAuthority).filter(HealthAuthority.email == email)
        authority = q.first()
        print(q.first().id)
        if authority is not None and authority.authenticate(password):
            login_user(authority)
            # this sets the global role variable
            session["role"] = "authority"
            return redirect("/")
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect("/")
