from flask.globals import session
from monolith.models import precautions
from flask.helpers import flash
from flask import Blueprint, redirect, render_template, request
from monolith.app import db
from monolith.models import Restaurant, Like, Precautions, RestaurantsPrecautions
from monolith.models.table import Table
from ..services.auth import admin_required, current_user, operator_required
from flask_login import current_user, login_user, logout_user, login_required
from ..services.forms import CreateRestaurantForm, CreateTableForm, UserForm
from ..controllers import restaurant


restaurants = Blueprint("restaurants", __name__)


@restaurants.route("/restaurants")
def _restaurants(message=""):
    allrestaurants = db.session.query(Restaurant)
    return render_template(
        "restaurants.html",
        message=message,
        restaurants=allrestaurants,
        role=session["role"],
        # base_url="http://127.0.0.1:5000/restaurants",
        base_url=request.base_url,
    )

@restaurants.route("/operator/restaurants")
@login_required
@operator_required
def operator_restaurants(message=""):
    operator_restaurants = db.session.query(Restaurant).filter_by(operator_id=current_user.id)
    return render_template(
        "restaurants.html",
        message=message,
        restaurants=operator_restaurants,
        role=session["role"],
        # base_url="http://127.0.0.1:5000/restaurants",
        base_url=request.base_url,
    )


@restaurants.route("/restaurants/<restaurant_id>")
def restaurant_sheet(restaurant_id):
    records = (
        db.session.query(Restaurant, Precautions, RestaurantsPrecautions)
        .filter(
            Restaurant.id == int(restaurant_id),
            Restaurant.id == RestaurantsPrecautions.restaurant_id,
            RestaurantsPrecautions.precautions_id == Precautions.id,
        )
        .all()
    )  # Join between tabels Restaurant, RestaurantsPrecautions and Precautions
    restaurant = records[0].Restaurant
    precautions = []
    for record in records:
        precautions.append(record.Precautions.name)
    return render_template(
        "restaurantsheet.html",
        name=restaurant.name,
        likes=restaurant.likes,
        lat=restaurant.lat,
        lon=restaurant.lon,
        phone=restaurant.phone,
        precautions=precautions,
    )


@restaurants.route("/restaurants/like/<restaurant_id>")
@login_required
def _like(restaurant_id):
    q = Like.query.filter_by(liker_id=current_user.id, restaurant_id=restaurant_id)
    if q.first() is not None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.restaurant_id = restaurant_id
        db.session.add(new_like)
        db.session.commit()
        message = ""
    else:
        message = "You've already liked this place!"
    return _restaurants(message)


@restaurants.route("/create_restaurant", methods=["GET", "POST"])
@login_required
@operator_required
def create_restaurant():
    status = 200
    form = CreateRestaurantForm()
    if request.method == "POST":

        if form.validate_on_submit():
            new_restaurant = Restaurant()
            form.populate_obj(new_restaurant)

            new_restaurant.likes = 0
            new_restaurant.operator_id = current_user.id
            
            if restaurant.add_new_restaurant(
                new_restaurant, 
                request.form.getlist("prec_measures")
            ):
                return redirect("operator/restaurants")
            else:
                flash("Restaurant already added", category="error")
                status = 400
        else:
            status = 400

    return render_template("create_restaurant.html", form=form), status


@restaurants.route("/restaurants/<restaurant_id>/tables")
@login_required
def _tables(restaurant_id):
    alltables = db.session.query(Table).filter_by(restaurant_id=restaurant_id)
    print(alltables.first())
    return render_template(
        "tables.html",
        tables=alltables,
        # base_url="http://127.0.0.1:5000/restaurants",
        base_url=request.base_url,
    )


@restaurants.route("/operator/restaurants/<restaurant_id>/create_table", methods=["GET", "POST"])
@login_required
@operator_required
def create_table(restaurant_id):
    status = 200
    form = CreateTableForm()
    if request.method == "POST":

        if restaurant.check_restaurant_ownership(
            current_user.id, 
            restaurant_id
        ):
            if form.validate_on_submit():
                new_table = Table()
                form.populate_obj(new_table)
                new_table.restaurant_id = restaurant_id
                
                if restaurant.add_new_table(new_table):
                    return redirect("/restaurants/" + restaurant_id + "/tables")
                else:
                    status = 400
                    flash("Table already added", category="error")
            else:
                status = 400
        else:
            status = 400
            flash("Can't add a table to a not owned restaurant", category="error")

    return render_template("create_table.html", form=form), status