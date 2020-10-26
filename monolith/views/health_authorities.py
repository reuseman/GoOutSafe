from flask import Blueprint, redirect, render_template, request
from monolith.database import db, HealthAuthority
from monolith.auth import admin_required
from monolith.forms import AuthorityForm

authorities = Blueprint("authorities", __name__)


@authorities.route("/authorities")
def _authorities():
    authority_list = db.session.query(HealthAuthority)
    return render_template("authorities.html", authorities=authority_list)


@authorities.route("/create_authority", methods=["GET", "POST"])
def create_authority():
    form = AuthorityForm()
    if request.method == "POST":

        if form.validate_on_submit():
            new_authority = HealthAuthority()
            form.populate_obj(new_authority)
            new_authority.set_password(
                form.password.data
            )  # pw should be hashed with some salt
            db.session.add(new_authority)
            db.session.commit()
            return redirect("/authorities")

    return render_template("create_health_authority.html", form=form)
