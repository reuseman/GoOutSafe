from monolith.views.auth import login
from flask import Blueprint, render_template, flash, redirect
from flask_login.utils import login_required

from monolith.app import db
from monolith.models import HealthAuthority, User
from ..services.auth import current_user, authority_required
from ..services.forms import MarkSsnForm, MarkEmailForm, MarkPhoneNumberForm

marks = Blueprint("marks", __name__)


@marks.route("/marks/new/ssn", methods=["GET", "POST"])
@authority_required
@login_required
def new_ssn_mark():
    status = 200
    form = MarkSsnForm()
    if form.validate_on_submit():
        ssn = form.ssn.data
        current_authority = current_user
        user_to_mark = User.query.filter_by(fiscal_code=ssn).first()
        if not user_to_mark:
            flash("User not found.")
        else:
            current_authority.mark(user_to_mark, form.duration.data)
            db.session.commit()

        return redirect("/marks/new/ssn")
    return render_template("mark_ssn.html", form=form), status


@marks.route("/marks/new/email", methods=["GET", "POST"])
@authority_required
@login_required
def new_email_mark():
    status = 200
    form = MarkEmailForm()
    if form.validate_on_submit():
        email = form.email.data
        current_authority = current_user
        user_to_mark = User.query.filter_by(email=email).first()
        if not user_to_mark:
            flash("User not found.")
        else:
            current_authority.mark(user_to_mark, form.duration.data)
            db.session.commit()

        return redirect("/marks/new/email")
    return render_template("mark_email.html", form=form), status


@marks.route("/marks/new/phonenumber", methods=["GET", "POST"])
@authority_required
@login_required
def new_phonenumber_mark():
    status = 200
    form = MarkPhoneNumberForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        current_authority = current_user
        user_to_mark = User.query.filter_by(phone_number=phone_number).first()
        if not user_to_mark:
            flash("User not found.")
        else:
            current_authority.mark(user_to_mark, form.duration.data)
            db.session.commit()

        return redirect("/marks/new/phonenumber")
    return render_template("mark_phonenumber.html", form=form), status
