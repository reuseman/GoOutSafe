from flask import Blueprint, redirect, render_template, request
from monolith.app import db
from monolith.models import User
from monolith.services.auth import admin_required
from monolith.services.forms import UserForm
from monolith.services.auth import authority_required

users = Blueprint("users", __name__)


@users.route("/users")
@authority_required
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/")

    return render_template("create_user.html", form=form)
