from flask import Blueprint, redirect, render_template, request
from monolith import db
from monolith.models import Operator
from monolith.services.auth import admin_required
from monolith.services.forms import OperatorForm

operators = Blueprint("operators", __name__)


@operators.route("/operators")
def _operators():
    operators = db.session.query(Operator)
    return render_template("operators.html", operators=operators)


@operators.route("/create_operator", methods=["GET", "POST"])
def create_operator():
    form = OperatorForm()
    if request.method == "POST":

        if form.validate_on_submit():
            new_operator = Operator()
            form.populate_obj(new_operator)
            db.session.add(new_operator)
            db.session.commit()
            return redirect("/")

    return render_template("create_operator.html", form=form)
