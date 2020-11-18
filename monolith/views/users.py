from flask import Blueprint, redirect, render_template, request
from monolith import db
from monolith.models import User
from monolith.services.forms import UserForm
from monolith.services.auth import authority_required

users = Blueprint("users", __name__)


@users.route("/users")
@authority_required
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route("/register/user", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(User.id).filter_by(email=form.email.data).scalar()
            if user is not None:
                return redirect("/login/user")
            else:
                new_user = User(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=form.password.data,
                    dateofbirth=form.dateofbirth.data,
                    phone_number=form.phone_number.data,
                    fiscal_code=form.fiscal_code.data,
                )

                db.session.add(new_user)
                db.session.commit()
                return redirect("/")

    return render_template("create_user.html", form=form)
