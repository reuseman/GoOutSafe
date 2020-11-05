from flask import Blueprint, redirect, render_template, request
from monolith import db
from monolith.models import Operator
from monolith.services.forms import OperatorForm

operators = Blueprint("operators", __name__)


@operators.route("/register/operator", methods=["GET", "POST"])
def create_operator():
    form = OperatorForm()
    if request.method == "POST":

        if form.validate_on_submit():
            operator = db.session.query(Operator.id).filter_by(email=form.email.data).scalar()
            if operator is not None:
                return redirect("/login/operator")
            else:
                new_operator = Operator(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=form.password.data,
                    dateofbirth=form.dateofbirth.data,
                    phone_number=form.phone_number.data,
                    fiscal_code=form.fiscal_code.data,
                )
                db.session.add(new_operator)
                db.session.commit()
                return redirect("/")

    return render_template("create_operator.html", form=form)
