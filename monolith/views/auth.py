from flask import Blueprint, render_template, redirect, session, flash
from flask_login import current_user, login_user, logout_user
from datetime import date


from monolith import db
from monolith.models import User, Operator, HealthAuthority
from monolith.services.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login/user", methods=["GET", "POST"])
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


@auth.route("/login/operator", methods=["GET", "POST"])
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


@auth.route("/login/authority", methods=["GET", "POST"])
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


@auth.route("/unsubscribe")
def unsubscribe():

    if current_user is None or not session.get("role"):
        return redirect("/login/user")

    if session["role"] == "user":
        user = db.session.query(User).filter(User.email == current_user.email).first()

        if user.is_marked():
            flash("Positive users cannot be deleted")
            return redirect("/")

        user.email = "deleted@deleted.it"
        user.firstname = "deleted"
        user.lastname = "deleted"
        user.password = "deleted"
        user.dateofbirth = date(2000, 1, 1)
        user.fiscal_code = "AAAAAAAAAAAAAAAA"
        user.phone_number = "+39333333333333"

    elif session["role"] == "operator":
        operator = (
            db.session.query(Operator)
            .filter(Operator.email == current_user.email)
            .first()
        )

        operator.email = "deleted@deleted.it"
        operator.firstname = "deleted"
        operator.lastname = "deleted"
        operator.password = "deleted"
        operator.dateofbirth = date(2000, 1, 1)
        operator.fiscal_code = "AAAAAAAAAAAAAAAA"
        operator.phone_number = "+39333333333333"

    logout_user()
    db.session.commit()
    return redirect("/")
