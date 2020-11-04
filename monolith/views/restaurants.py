from flask.globals import session
from monolith.models import precautions
from flask.helpers import flash
from flask import Blueprint, redirect, render_template, request, url_for
from monolith import db
from monolith.models import Restaurant, Like, Precautions, RestaurantsPrecautions
from monolith.models.menu import Menu, Food, FoodCategory
from monolith.models.table import Table
from monolith.services.auth import admin_required, current_user, operator_required
from flask_login import current_user, login_user, logout_user, login_required
from monolith.services.forms import (
    CreateRestaurantForm,
    CreateTableForm,
    ReviewForm,
    UserForm,
)
from ..controllers import restaurant

restaurants = Blueprint("restaurants", __name__)


@restaurants.route("/restaurants")
def _restaurants(message=""):
    allrestaurants = db.session.query(Restaurant)
    if current_user.is_authenticated:
        role = session["role"]
    else:
        role = ""

    return render_template(
        "restaurants.html",
        message=message,
        restaurants=allrestaurants,
        role=role,
        # base_url="http://127.0.0.1:5000/restaurants",
        base_url=request.base_url,
    )


@restaurants.route("/operator/restaurants")
@login_required
@operator_required
def operator_restaurants(message=""):
    operator_restaurants = db.session.query(Restaurant).filter_by(
        operator_id=current_user.id
    )
    return render_template(
        "restaurants.html",
        message=message,
        restaurants=operator_restaurants,
        role=session["role"],
        # base_url="http://127.0.0.1:5000/restaurants",
        base_url=request.base_url,
    )


@restaurants.route("/restaurants/<restaurant_id>", methods=["GET", "POST"])
def restaurant_sheet(restaurant_id):
    q_restaurant = (
        db.session.query(Restaurant).filter_by(
            id=int(restaurant_id)
        )
        .first()
    )
    q_restaurant_precautions= db.session.query(Precautions.name).filter(
        Precautions.id == RestaurantsPrecautions.precautions_id,
        RestaurantsPrecautions.restaurant_id == int(restaurant_id)
    ).all()

    precautions = []
    for prec in q_restaurant_precautions:
        precautions.append(prec.name)

    # REVIEWS
    # TODO sort them by the most recent, or are they already in that order
    # TODO show in the view the date of the review
    reviews = q_restaurant.reviews
    form = ReviewForm()
    if form.is_submitted():
        if current_user.is_anonymous:
            flash("To review the restaurant you need to login.")
            return redirect(url_for('auth.login'))
        if form.validate():
            if session["role"] != "user":
                flash("Only a logged user can review a restaurant.")
            else:
                # Check if the user already did a review
                if current_user.already_reviewed(q_restaurant):
                    flash("You already reviewed this restaraunt")
                else:
                    rating = form.rating.data
                    message = form.message.data
                    current_user.review(q_restaurant, rating, message)
                    db.session.commit()
                    return redirect("/restaurants/" + restaurant_id)

    return render_template(
        "restaurantsheet.html",
        id=q_restaurant.id,
        name=q_restaurant.name,
        likes=q_restaurant.likes,
        lat=q_restaurant.lat,
        lon=q_restaurant.lon,
        phone=q_restaurant.phone,
        precautions=precautions,
        menus=q_restaurant.menus,
        # base_url="http://127.0.0.1:5000/restaurants/<restaurant_id>",
        base_url=request.base_url,
        reviews=reviews,
        form=form,
    )


@restaurants.route("/restaurants/like/<restaurant_id>")
@login_required
def _like(restaurant_id):
    q = Like.query.filter_by(liker_id=current_user.id,
                             restaurant_id=restaurant_id)
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
                    new_restaurant, request.form.getlist("prec_measures")
            ):
                return redirect("operator/restaurants")
            else:
                flash("Restaurant already added", category="error")
                status = 400
        else:
            status = 400

    return render_template("create_restaurant.html", form=form), status


@restaurants.route("/operator/restaurants/<restaurant_id>/create_menu", methods=["GET", "POST"])
@login_required
@operator_required
def create_menu(restaurant_id):
    status = 200
    
    if request.method == "POST":
        menu = Menu()
        menu.name = request.form["menu_name"]

        if menu.name == "":
            flash("No empty menu name!", category="error")
            status = 400

        q = db.session.query(Menu).filter_by(name=menu.name).first()
        if q is None and status == 200:
            menu.restaurant_id = int(restaurant_id)

            food_names = set()
            for name, price, category in zip(request.form.getlist('name'), 
                                            request.form.getlist('price'), 
                                            request.form.getlist('category')):
                food = Food()
                food.name = name
                food.category = category
                print(food.category)
                choices = [i[0] for i in FoodCategory.choices()]
                try:
                    food.price = float(price)
                    is_float = True
                except ValueError:
                    is_float = False
                
                if not is_float:
                    flash("Not a valid price number", category="error")
                    status = 400
                elif food.price < 0:
                    flash("No negative values!", category="error")
                    status = 400
                elif food.name == "":
                    flash("No empty food name!", category="error")
                    status = 400
                elif food.category not in choices:
                    flash("Wrong category selected!", category="error")
                    status = 400
                elif food.name in food_names:
                    flash("No duplicate food name!", category="error")
                    status = 400
                else:
                    menu.foods.append(food)
                    food_names.add(food.name)

            if status == 200:
                db.session.add(menu)
                db.session.commit()
                return redirect("/operator/restaurants")
        else:
            status = 400
            flash("There is already a menu with the same name!", category="error")

    return render_template("create_menu.html", choices=FoodCategory.choices()), status


@restaurants.route("/restaurants/<restaurant_id>/show_menu/<menu_id>", methods=["GET", "POST"])
def show_menu(restaurant_id, menu_id):
    q_restaurant_menu = db.session.query(Menu).filter(Menu.restaurant_id == restaurant_id,
        Menu.id == menu_id).first()

    return render_template("show_menu.html", menu=q_restaurant_menu)


@restaurants.route("/restaurants/<restaurant_id>/tables")
@login_required
@operator_required
def _tables(restaurant_id):
    status = 200
    if restaurant.check_restaurant_ownership(current_user.id, restaurant_id):
        alltables = db.session.query(Table).filter_by(
            restaurant_id=restaurant_id)
    else:
        status = 401

    return (
        render_template(
            "tables.html",
            tables=alltables,
            # base_url="http://127.0.0.1:5000/restaurants",
            base_url=request.base_url,
        ),
        status,
    )


@restaurants.route(
    "/operator/restaurants/<restaurant_id>/create_table", methods=["GET", "POST"]
)
@login_required
@operator_required
def create_table(restaurant_id):
    status = 200
    form = CreateTableForm()
    if request.method == "POST":

        if restaurant.check_restaurant_ownership(current_user.id, restaurant_id):
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


@restaurants.route(
    "/operator/restaurants/<restaurant_id>/tables/<table_id>/edit_table",
    methods=["GET", "POST"],
)
@login_required
@operator_required
def edit_table(restaurant_id, table_id):
    status = 400
    form = CreateTableForm()
    if request.method == "POST":

        if restaurant.check_restaurant_ownership(current_user.id, restaurant_id):
            if form.validate_on_submit():
                new_table = Table()
                form.populate_obj(new_table)
                new_table.restaurant_id = restaurant_id
                new_table.id = table_id

                if restaurant.check_table_existence(new_table):
                    if restaurant.edit_table(new_table):
                        status = 200
                        return redirect("/restaurants/" + restaurant_id + "/tables")
                    else:
                        flash(
                            "There is already a table with the same name!",
                            category="error",
                        )
        else:
            flash("Can't edit a table of a not owned restaurant", category="error")

    return render_template("create_table.html", form=form), status


@restaurants.route(
    "/operator/restaurants/<restaurant_id>/tables/<table_id>/delete_table",
    methods=["GET", "POST"],
)
@login_required
@operator_required
def delete_table(restaurant_id, table_id):
    status = 400
    if restaurant.check_restaurant_ownership(current_user.id, restaurant_id):
        table = Table(id=table_id)

        if restaurant.delete_table(table):
            status = 200
            return redirect("/restaurants/" + restaurant_id + "/tables")
        else:
            flash("The table to be deleted does not exist!", category="error")
    else:
        flash("Can't delete a table of a not owned restaurant", category="error")

    return redirect("/restaurants/" + restaurant_id + "/tables"), status
