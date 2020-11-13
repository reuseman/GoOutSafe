from sqlalchemy.util.compat import u
from monolith.views.auth import login
from flask import Blueprint, render_template, flash, redirect
from flask_login.utils import login_required

from monolith import db
from monolith.models import HealthAuthority, User
from monolith.services.auth import current_user, authority_required
from monolith.services.forms import (
    ContactTracingPhoneNumberForm,
    MarkSsnForm,
    MarkEmailForm,
    MarkPhoneNumberForm,
)

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
            flash("User not found.", category="error")
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
            flash("User not found.", category="error")
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
            flash("User not found.", category="error")
        else:
            current_authority.mark(user_to_mark, form.duration.data)
            db.session.commit()

        return redirect("/marks/new/phonenumber")
    return render_template("mark_phonenumber.html", form=form), status


@marks.route("/trace/phonenumber", methods=["GET", "POST"])
@authority_required
@login_required
def trace_by_phonenumber():
    # return user
    # return object
    # { "date", datetiem)
    contacts = []
    form = ContactTracingPhoneNumberForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            flash("The user was not found", category="error")
        else:
            if user.is_marked():
                user_bookings = user.get_bookings(range_duration=form.interval.data)

                for user_booking in user_bookings:
                    contacts_temp = []
                    starting_time = user_booking.start_booking
                    restaurant = user_booking.table.restaurant
                    restaurant_bookings = restaurant.get_bookings(starting_time)
                    for b in restaurant_bookings:
                        if b.user != user:
                            contacts_temp.append(b.user)
                    if contacts_temp:
                        contacts.append(
                            {"date": starting_time, "people": contacts_temp}
                        )

                if not contacts:
                    flash("The user did not have any contact", category="info")
            else:
                flash("You cannot trace a user that is not marked", category="error")

    return render_template("trace_phonenumber.html", form=form, contacts=contacts)
