from flask.globals import session
from monolith.models import precautions
from flask.helpers import flash
from flask import Blueprint, redirect, render_template, request, url_for, make_response
from monolith import db
from monolith.models import Restaurant, Like, Precautions, RestaurantsPrecautions,Table, User, Booking
from monolith.models.menu import Menu, Food, FoodCategory
from monolith.models.table import Table
from monolith.services.auth import admin_required, current_user, operator_required, user_required
from flask_login import current_user, login_user, logout_user, login_required
from monolith.services.forms import (
    CreateRestaurantForm,
    CreateTableForm,
    ReviewForm,
    UserForm,
    CreateBookingDateHourForm,
    ConfirmBookingForm
)
from ..controllers import restaurant
from datetime import date, timedelta, datetime
from sqlalchemy import func 
from flask_login import current_user

restaurants = Blueprint("restaurants", __name__)

booking_number=-1

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
        open=q_restaurant.opening_hours,
        close=q_restaurant.closing_hours,
        cuisine=q_restaurant.cuisine_type.value,
        menus=q_restaurant.menus,
        base_url=request.base_url,
        reviews=reviews,
        form=form,
    )


@restaurants.route("/restaurants/<restaurant_id>/book_table", methods=["GET","POST"])
@login_required
@user_required
def book_table_form(restaurant_id):
    form = CreateBookingDateHourForm()
    max_table_seats = db.session.query(func.max(Table.seats)).filter(Table.restaurant_id==restaurant_id).first()[0] #Take max seats from tables of restaurant_ud
    time=[]
    range_hour=db.session.query(Restaurant.time_of_stay).filter_by(id=restaurant_id).first()[0]
    for i in range(480,1320,range_hour):
        time.append(str(timedelta(minutes=i))[:-3]+" - "+str(timedelta(minutes=i+range_hour))[:-3])
    
    if request.method == "POST":
        if form.validate_on_submit():
            number_persons = int(request.form["number_persons"])
            booking_hour_start = request.form["booking_hour"].split(" - ")[0]
            booking_hour_end = request.form["booking_hour"].split(" - ")[1]
            booking_date = request.form["booking_date"]
            booking_date_start=datetime.strptime(booking_date+" "+booking_hour_start, '%Y-%m-%d %H:%M') 
            booking_date_end=datetime.strptime(booking_date+" "+booking_hour_end, '%Y-%m-%d %H:%M') 

            restaurant = db.session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            table = restaurant.get_free_table(number_persons,booking_date_start)
            
            if table is None:
                flash("No tables avaible for "+str(number_persons)+" people for this date and time")
            else:
                global booking_number
                if booking_number == -1:
                    booking_number = db.session.query(func.max(Booking.booking_number)).first()[0]
                    booking_number+=1

                confirmed_bookign = True if number_persons==1 else False                    
                db.session.add(Booking(user_id=current_user.id, table_id=table, booking_number=booking_number, start_booking=booking_date_start, end_booking=booking_date_end, confirmed_booking=confirmed_bookign))
                db.session.commit()
            
                old_booking_number = booking_number
                booking_number+=1

                if confirmed_bookign:
                    flash("Booking confirmed")
                    return redirect("/restaurants")
                else:
                    session['booking_number']=old_booking_number
                    session['number_persons']=number_persons
                    return(redirect(url_for('.confirm_booking', restaurant_id=restaurant_id)))
        else:
            flash("Are you really able to go back to the past?") 
            
    return render_template("book_table.html", form=form, max_table_seats=max_table_seats, hours_list=time)


@restaurants.route("/restaurants/<restaurant_id>/book_table/confirm", methods=["GET","POST"])
@login_required
@user_required
def confirm_booking(restaurant_id):
    booking_number=session["booking_number"]
    number_persons=session['number_persons']
    form = ConfirmBookingForm(number_persons-1)
    error = False

    if form.validate_on_submit():
        booking = db.session.query(Booking).filter_by(booking_number=booking_number).first()

        for i, field in enumerate(form.people):
            user = db.session.query(User).filter_by(fiscal_code=field.fiscal_code.data).first()
            if user is None:
                if db.session.query(User).filter_by(email=field.email.data).first() is None: #check if email is already in the db or not
                    user = User(firstname=field.firstname.data, lastname=field.lastname.data, email=field.email.data, fiscal_code=field.fiscal_code.data)
                    db.session.add(user)
                    db.session.commit()
                else:
                    flash("Person "+str(i+1)+ ", mail already used from another from a registered user")
                    error = True
                    break
            else:
                if not user.check_equality_for_booking(field.firstname.data, field.lastname.data, field.email.data): #if the user exists, check if the data filled are correct
                    flash("Person "+str(i+1)+ ", incorrect data")
                    error = True
                    break
                if booking.user_already_booked(user.id):
                    flash("Person "+str(i+1)+ ", user already registered in the booking")
                    error = True
                    break
            db.session.add(Booking(user_id=user.id, table_id=booking.table_id, booking_number=booking.booking_number, start_booking=booking.start_booking, end_booking=booking.end_booking, confirmed_booking=True))
        
        if error:
            db.session.rollback()
        else:
            booking.confirmed_booking=True
            db.session.commit()

            session.pop('booking_number', None)
            session.pop('number_persons', None)
            flash("Booking confirmed")
            return redirect('/restaurants')

    return render_template("confirm_booking.html", form=form, number_persons=int(number_persons))


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
    
    zipped = None
    name = ""
    if request.method == "POST":
        menu = Menu()
        menu.name = request.form["menu_name"]
        name = request.form["menu_name"]

        if menu.name == "":
            flash("No empty menu name!", category="error")
            status = 400

        q = db.session.query(Menu).filter_by(name=menu.name).first()
        if q is None and status == 200:
            menu.restaurant_id = int(restaurant_id)

            food_names = set()
            zipped = zip(request.form.getlist('name'), 
                        request.form.getlist('price'), 
                        request.form.getlist('category'))
            for name, price, category in zipped:
                food = Food()
                food.name = name
                food.category = category
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

    if zipped or name:
        zip_to_send = zip(request.form.getlist('name'), 
                        request.form.getlist('price'), 
                        request.form.getlist('category'))
                        
        return render_template("create_menu.html", choices=FoodCategory.choices(), 
            items=zip_to_send, menu_name=name), status
    else:
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
