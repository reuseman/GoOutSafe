from flask import Blueprint, redirect, render_template, request
from monolith import db
from monolith.models import HealthAuthority
from monolith.services.forms import AuthorityForm

authorities = Blueprint("authorities", __name__)


@authorities.route("/register/authority", methods=["GET", "POST"])
def create_authority():
    form = AuthorityForm()
    if request.method == "POST":
        if form.validate_on_submit():
            authority = (
                db.session.query(HealthAuthority.id)
                .filter_by(email=form.email.data)
                .scalar()
            )
            if authority is not None:
                return redirect("/login/authority")
            else:
                new_authority = HealthAuthority()
                form.populate_obj(new_authority)
                db.session.add(new_authority)
                db.session.commit()
                return redirect("/")

    return render_template("create_health_authority.html", form=form)
